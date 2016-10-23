import types
from troposphere import Template, FindInMap, Ref, Parameter
from collections import defaultdict
from . import config

__all__ = ['base_template', 'add_parameter', 'add_instance']

base_version = config['base']['version']
base_description = config['base']['description']


def base_template(fn):
    template = add_metadata_handlers(Template())
    template.add_version(base_version)
    template.add_description(base_description)
    return fn(template)


def add_metadata_handlers(template):
    def add_parameter_metadata(self, parameter_name, parameter_value):
        self._metadata['parameters'][parameter_name] = parameter_value

    def get_parameter_metadata(self):
        return self._metadata['parameters']

    def add_instance_metadata(self, instance_name, instance_value):
        self._metadata['instances'][instance_name] = instance_value

    def get_instance_metadata(self):
        return self._metadata['instances']

    def add_security_group_metadata(self, security_group_name, security_group_value):
        self._metadata['security_groups'][security_group_name] = security_group_value

    def get_security_group_metadata(self):
        return self._metadata['security_groups']

    template._metadata = {
        'maps': defaultdict(lambda: None),
        'parameters': defaultdict(lambda: None),
        'instances': defaultdict(lambda: None),
        'security_groups': defaultdict(lambda: None)
    }
    template.get_parameter_metadata = types.MethodType(get_parameter_metadata, template)
    template.add_parameter_metadata = types.MethodType(add_parameter_metadata, template)
    template.get_instance_metadata = types.MethodType(get_instance_metadata, template)
    template.add_instance_metadata = types.MethodType(add_instance_metadata, template)
    template.get_security_group_metadata = types.MethodType(get_security_group_metadata, template)
    template.add_security_group_metadata = types.MethodType(add_security_group_metadata, template)
    return template

