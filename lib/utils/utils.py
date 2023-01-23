import yaml
import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)


def get_set_up_config(filepath) -> dict:
    with open(filepath, 'r') as stream:
        dictionary = yaml.safe_load(stream)

    return dictionary


def get_config(*filepaths) -> ConfigParser:
    config_parser = ConfigParser()
    for filepath in filepaths:
        config_parser.read(filepath)

    return config_parser
