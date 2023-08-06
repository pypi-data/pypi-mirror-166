""" dj - Docker-Jinja """

# init python std logging
import logging
import logging.config
import os

__version__ = "1.0.0"


# Set to True to have revision from Version Control System in version string
__devel__ = True


# Global register dict of all registered methods and filters
# NOTE: This must be here so that it will be properly visible for all code and to make it work properly
_local_env = {
    "globals": {},
    "filters": {},
}

log_level_to_string_map = {5: "DEBUG", 4: "INFO", 3: "WARNING", 2: "ERROR", 1: "CRITICAL", 0: "INFO"}


def init_logging(log_level):
    """
    Init logging settings with default set to INFO
    """
    level = log_level_to_string_map[log_level]

    msg = "%(levelname)s - %(name)s:%(lineno)s - %(message)s" if level in os.environ else "%(levelname)s - %(message)s"

    logging_conf = {
        "version": 1,
        "root": {"level": level, "handlers": ["console"]},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "formatters": {"simple": {"format": f" {msg}"}},
    }

    logging.config.dictConfig(logging_conf)


__all__ = ["init_logging", "_local_env", "__version__"]
