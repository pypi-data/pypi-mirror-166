# python std lib
import json
import logging
import os

import yaml

log = logging.getLogger(__name__)


class ConfTree(object):
    def __init__(self, config_files=None):
        self.config_files = config_files if config_files else []
        if not isinstance(self.config_files, list):
            raise Exception("config files must be a list of items that can be read from FS")
        self.tree = {}

    def load_config_files(self):
        for config_file in self.config_files:
            try:
                self.load_config_file(config_file)
            except Exception:
                log.debug(f"unable to load default config file : {config_file}")
                pass

    def load_config_file(self, config_file):
        if not os.path.exists(config_file):
            raise Exception("Path to config file do not exists on disk...")

        with open(config_file, "r") as stream:
            data = stream.read()

        if not data:
            raise Exception(f"No data in config file : {config_file}")

        # Try first with yaml as that is default config lagn
        # If yaml loading failed then try json loading
        try:
            data_tree = yaml.loads(data)
        except Exception:
            try:
                data_tree = json.loads(data)
            except Exception:
                raise Exception(f"Unable to load data as yaml or json from config file : {config_file}")

        log.debug(f"Loading default data from default config file : {config_file}")

        # If data was loaded into python datastructure then load it into the config tree
        self.merge_data_tree(data_tree)

    @classmethod
    def __update_dict(cls, d, u):
        import collections.abc

        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = cls.__update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def merge_data_tree(self, data_tree):
        if not isinstance(data_tree, dict):
            raise Exception("Data tree to merge must be of dict type")

        self.__update_dict(self.tree, data_tree)

    def get_tree(self):
        return self.tree

    def get(self, key, default=None):
        return self.tree.get(key, default) or self.tree.get("env", {}).get(key, default)
