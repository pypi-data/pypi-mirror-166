import logging
import os
import sys

# 3rd party imports
from jinja2 import Template

# Package imports
from . import _local_env, contrib
from .conftree import ConfTree

log = logging.getLogger(__name__)


class Core(object):
    def __init__(self, cli_args):
        """
        :param cli_args: Arguments structure from docopt.
        """
        self.args = cli_args

        log.debug(f"Cli args: {self.args}")

        self.default_config_files = [
            "/etc/dj.yaml",
            "/etc/dj.json",
            os.path.expanduser("~/.dj.yaml"),
            os.path.expanduser("~/.dj.json"),
            os.path.join(os.getcwd(), ".dj.yaml"),
            os.path.join(os.getcwd(), ".dj.json"),
        ]

        log.debug(f"DEFAULT_CONFIG_FILES: {self.default_config_files}")

        self.outfile = ""

        # Load all config files into unified config tree
        log.debug("Building config...")
        self.config = ConfTree(self.default_config_files)
        self.config.load_config_files()
        log.debug("Config building is done")

    def parse_env_vars(self):
        """
        Parse all variables inputted from cli and add them to global config
        """
        env_vars = {}
        for var in self.args.get("--env", []):
            s = var.split("=")
            if len(s) != 2 or (len(s[0]) == 0 or len(s[1]) == 0):
                raise Exception(f"var '{var}' is not of format 'key=value'")
            env_vars[s[0]] = s[1]
        self.config.merge_data_tree({"env": env_vars})

    def load_user_specefied_config_file(self):
        """
        Loads any config file specefied by user from commandline.

        It should only be possible to load one user specefied config file.
        """
        user_specefied_config_file = self.args.pop("--config", None)
        if user_specefied_config_file:
            log.debug(f"Loading user specified config file : {user_specefied_config_file}")
            self.config.load_config_file(user_specefied_config_file)

    def handle_data_sources(self):
        """
        Take all specefied datasources from cli and merge with any in config then
        try to import all datasources and raise exception if it fails.
        """
        # TODO: Push datasources into conftree but because they are lists they wont merge easy
        #  via dict.update()
        ds = self.args.get("--datasource", [])
        ds.extend(self.config.tree.get("datasources", []))

        # Find all contrib files and add them to datasources to load
        ds.extend([getattr(contrib, c).__file__ for c in dir(contrib) if not c.startswith("_")])

        # Load all specefied datasource files
        for datasource_file in ds:
            if not os.path.exists(datasource_file):
                raise Exception(f"Unable to load datasource file : {datasource_file}")

            p = os.path.dirname(datasource_file)

            try:
                # Append to sys path so we can import the python file
                sys.path.insert(0, p)
                datasource_path = os.path.splitext(os.path.basename(datasource_file))[0]
                log.debug(f"{datasource_path}")

                # Import python file but do nothing with it because all datasources should
                #  handle and register themself to jinja.
                i = __import__(datasource_path)

                # Auto load all filters and global functions if they follow name pattern
                for method in dir(i):
                    if method.lower().startswith("_filter_"):
                        method_name = method.replace("_filter_", "")
                        self._attach_function("filters", getattr(i, method), method_name)
                    elif method.lower().startswith("_global_"):
                        method_name = method.replace("_global_", "")
                        self._attach_function("globals", getattr(i, method), method_name)
            except ImportError as ie:
                log.critical(f"cannot load datasource. {ie}")
                raise ie
            finally:
                # Clean out path to avoid issue
                sys.path.remove(p)

    def process_dockerfile(self):
        """
        Read source dockerfile --> Render with jinja --> Write to outfile
        """
        source_dockerfile = self.args["--dockerfile"]

        with open(source_dockerfile, "r") as stream:
            log.info("Reading source file...")
            template = Template(stream.read())

        # Update the jinja environment with all custom functions & filters
        self._update_env(template.environment)

        context = self.config.get("env", {})
        log.info("Rendering context")

        for k, v in context.items():
            log.info(f"  * {k}: {v}")

        log.info("Rendering Dockerfile...")
        out_data = template.render(**context)

        log.debug("\n******\nWriting to file\n*******")
        log.debug(out_data)

        if "--outfile" not in self.args:
            log.debug("No --outfile <FILE> was specified. Defaulting to Dockerfile")
            self.outfile = "Dockerfile"
        else:
            self.outfile = self.args["--outfile"]

        with open(self.outfile, "w") as stream:
            log.info("Writing to outfile...")
            stream.write(out_data)

    def _attach_function(self, attr, func, name):
        """
        Register a function so it can be used within Jinja
        """
        log.debug(f"Attaching function to jinja : {attr} : {func.__name__} : {name}")

        global _local_env
        _local_env[attr][name] = func
        return func

    def _update_env(self, env):
        """
        Given a jinja environment, update it with third party
        collected environment extensions.
        """
        env.globals.update(_local_env["globals"])
        env.filters.update(_local_env["filters"])

    def main(self):
        """
        Runs all logic in application
        """
        self.load_user_specefied_config_file()

        self.parse_env_vars()

        self.handle_data_sources()

        self.process_dockerfile()

        log.info("Done... Bye :]")
