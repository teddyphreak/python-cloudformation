import os
import urllib.request
import pytest

from nephelaiio.cloudformation.test.helpers import \
    template_files, read_template, validate_template, cloudformation_client, create_stack, delete_stack, \
    test_region

ec2_client = cloudformation_client(test_region)


@pytest.mark.parametrize("template_file", [os.path.join('test', 'templates', 'dummy.yml')])
def test_template_files(template_file):
    assert template_file in template_files


@pytest.mark.parametrize(
    "template_file,template_body",
    [(os.path.join('test', 'templates', 'dummy.yml'), '---\n')])
def test_read_template(template_file, template_body):
    assert read_template(template_file) == template_body


template_url = 'https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2/' \
               'S3_Website_Bucket_With_Retain_On_Delete.template'
with urllib.request.urlopen(template_url) as response:
    sample_template_body = response.read().decode('utf-8')


@pytest.mark.parametrize(
    "client,template_body,success",
    [(ec2_client, sample_template_body, True)])
def test_validate_template(client, template_body, success):
    assert validate_template(client, template_body) == success


@pytest.mark.parametrize(
    "client,template_body,stack_name,create_status,delete_status",
    [(ec2_client, sample_template_body, 'test-create-template', 'CREATE_COMPLETE', 'DELETE_COMPLETE')]
)
def test_template_lifecycle(client, template_body, stack_name, create_status, delete_status):
    assert delete_stack(client, stack_name) == delete_status
    assert create_stack(client, template_body, stack_name) == create_status
    assert delete_stack(client, stack_name) == delete_status
