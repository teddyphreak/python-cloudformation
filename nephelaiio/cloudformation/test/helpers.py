import os
import re
import boto3
from time import sleep
from functools import reduce


_TEMPLATE_DIR = ['templates', 'test/templates']

template_dirs = filter(lambda f: os.path.exists(f), _TEMPLATE_DIR)
template_dir_files = reduce(lambda x, y: x + y, [], [os.path.join(y, x) for y in template_dirs for x in os.listdir(y)])
template_files = [x for x in template_dir_files if re.match('.*\.(yml|json)$', x)]
stack_status_deleted = 'DELETE_COMPLETE'
test_region = 'us-west-2'


def read_template(template_file):
    with open(template_file, 'r') as tpl:
        return tpl.read()


def cloudformation_client(region):
    return boto3.client('cloudformation')


def validate_template(client, template_body):
    return 'Description' in client.validate_template(TemplateBody=template_body)


def delete_stack(client, stack_name, delete_wait_secs=30):
    stack_status = stack_status_deleted
    if filter(lambda x: x['StackName'] == stack_name, client.describe_stacks()['Stacks']):
        client.delete_stack(StackName=stack_name)
        sleep(delete_wait_secs)
        stack_status = describe_stack(client, stack_name)
    return stack_status


def describe_stack(client, stack_name):
    stacks = client.describe_stacks()['Stacks']
    target_stack = [x for x in stacks if x['StackName'] == stack_name]
    return target_stack and target_stack[0]['StackStatus'] or stack_status_deleted


def create_stack(client, template_body, stack_name, timeout_period_num=5, timeout_period_secs=60):
    client.create_stack(
        StackName=stack_name, 
        TemplateBody=template_body, 
        TimeoutInMinutes=timeout_period_num * timeout_period_secs)
    retries = timeout_period_num
    stack_status = describe_stack(client, stack_name)
    while stack_status == "CREATE_IN_PROGRESS" and retries > 0:
        sleep(timeout_period_secs)
        retries -= 1
        stack_status = describe_stack(client, stack_name)
    return stack_status


def validate_stack(client, template_body, validate_fn, stack_name='testy-prober'):
    delete_stack(client, stack_name)
    create_stack(client, template_body, stack_name)
    assert validate_fn()
    delete_stack(client, stack_name)
