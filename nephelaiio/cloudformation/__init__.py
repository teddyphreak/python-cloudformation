import pkg_resources
import configparser
import os

__all__ = ['config']

config = configparser.ConfigParser()
default_config_data = pkg_resources.resource_filename(__name__, 'defaults.cfg')
override_config_data = os.path.expanduser('~/.nephelaiio/cloudformation.cfg')
config.read([default_config_data, override_config_data])
