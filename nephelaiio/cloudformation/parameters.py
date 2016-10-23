from troposphere import Parameter
from . import config

keyname_name = config['keyname']['name']
keyname_description = config['keyname']['description']
keyname_type = config['keyname']['type']

def add_parameter(template, parameter_name, parameter_description, parameter_type):
    if not template.get_parameter_metadata(parameter_name):
        new_parameter = Parameter(parameter_name, parameter_description, parameter_type)
        template.set_parameter_metadata(parameter_name, new_parameter)
        template.add_resource(new_parameter)
    return template


def add_keyname_parameter(template):
    return add_parameter(template, keyname_name, keyname_description, keyname_type)

