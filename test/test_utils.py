import sys
import os
import pytest
import urllib.request

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

from utils import template_files, read_template, validate_template


@pytest.mark.parametrize("template_file", [os.path.join('test', 'templates', 'dummy.yml')])
def test_template_files(template_file):
    assert template_file in template_files


@pytest.mark.parametrize(
    "template_file,template_body",
    [(os.path.join('test', 'templates', 'dummy.yml'), '---\n')])
def test_read_template(template_file, template_body):
    assert read_template(template_file) == template_body


template_url = 'https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2' + \
    '/EC2InstanceWithSecurityGroupSample.template'
with urllib.request.urlopen(template_url) as response:
    template_body = response.read().decode('utf-8')


@pytest.mark.parametrize(
    "template_body,region,success",
    [(template_body, 'us-west-2', True)])
def test_validate_template(template_body, region, success):
    assert validate_template(template_body, region) == success
