from troposphere import Ref, FindInMap
from troposphere.ec2 import Instance
from .parameters import  add_keyname_parameter
from . import config

keyname_name = config['keyname']['name']
regionmap_name = config['regionmap']['name']
regionmap_key = config['regionmap']['key']
sshsg_name = config['securitygroup_ssh']['name']
sshsg_description = config['securitygroup_ssh']['description']


def add_instance(template, instance_name, instance_type, security_group='default'):
    template = add_keyname_parameter(template)
    if not template.get_instance_metadata(instance_name):
        new_instance = Instance(
            instance_name,
            ImageId=FindInMap(regionmap_name, Ref('AWS::Region'), regionmap_key),
            InstanceType=instance_type,
            KeyName=Ref(template.get_parameter_metadata(keyname_name))
        )
        template.set_instance_metadata(instance_name, new_instance)
        template.add_resource(new_instance)
    return template
