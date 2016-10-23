from troposphere.ec2 import SecurityGroup, SecurityGroupRule
from . import config

sshsg_name = config['securitygroup_ssh']['name']
sshsg_description = config['securitygroup_ssh']['description']


def add_open_ssh_security_group(template):
    if not template.get_security_group_metadata(sshsg_name):
        new_security_group = SecurityGroup(
            sshsg_name,
            sshsg_description,
            SecurityGroupIngress=[
                SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='22',
                    ToPort='22',
                    CidrIp='0.0.0.0/0'
                )
            ]
        )
        template.add_security_group_metadata(sshsg_name, new_security_group)
        template.add_resource(new_security_group)
