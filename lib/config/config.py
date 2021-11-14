import os
from configparser import ConfigParser

path_to_config = os.path.join("lib", "config", "files")

config = ConfigParser()
config.read(os.path.join(path_to_config, "sysconfig.ini"))
config.read(os.path.join(path_to_config, "userconfig.ini"))
config.read(os.path.join(path_to_config, "keys.ini"))