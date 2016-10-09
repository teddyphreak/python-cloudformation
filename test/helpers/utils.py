import os
import re
import boto3
from functools import reduce


_TEMPLATE_DIR = ['templates', 'test/templates']


template_dir_files = reduce(lambda x, y: x + y, [], [os.path.join(y, x) for y in _TEMPLATE_DIR for x in os.listdir(y)])
template_files = [x for x in template_dir_files if re.match('.*\.(yml|json)$', x)]


def read_template(template_file):
    with open(template_file, 'r') as tpl:
        return(tpl.read())

def cloudformation_client(region):
    return(boto3.client('cloudformation'))


def validate_template(client, template_body):
    return('Description' in client.validate_template(TemplateBody=template_body))


def delete_stack(client, stack_name, delete_wait_secs=30):
    if filter(lambda x: x['StackName'] == stack_name, client.describe_stacks()['Stacks']):
        client.delete_stack(StackName=stack_name)
        sleep(delete_wait)


def describe_stack(client, stack_name):
    return(client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus'])


def create_stack(client, template_body, stack_name,
        timeout_period_num=5,
        timeout_period_secs=60):
    client.create_stack(
        StackName=stack_name, 
        TemplateBody=template_body, 
        TimeoutInMinutes=timeout_period_num * timeout_period_secs)
    retrues = timeout_period_num
    stack_status = describe_stack(client, stack_name)
    while stack_status == "CREATE_IN_PROGRESS" and retries > 0:
        sleep(timeout_period_secs)
        retries -= 1
        stack_status = describe_stack(client, stack_name)
    return stack_status

def validate_stack(client, template_body, validate_fn, stack_name='testy-prober'):
    delete_stack(client, stack_name)
    create_stack(client, template_body, stack_name)
    delete_stack(client, stack_name)
