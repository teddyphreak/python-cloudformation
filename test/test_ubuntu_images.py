import pytest

from nephelaiio.cloudformation.test.helpers import test_region
from nephelaiio.cloudformation.images.ubuntu \
    import get_image_data, get_image_map


@pytest.mark.parametrize('release,source', [
    ('xenial', 'released.current.txt'),
    ('trusty', 'released.current.txt'),
    ('xenial', 'released.txt'),
    ('trusty', 'released.txt'),
    ('xenial', 'daily.current.txt'),
    ('trusty', 'daily.current.txt'),
    ('xenial', 'daily.txt'),
    ('trusty', 'daily.txt')
])
def test_get_image_data(release, source):
    image_data = get_image_data(release, source)
    assert type(image_data) == list
    assert image_data != []


@pytest.mark.parametrize('image_data,instance_type', [
    (get_image_data('xenial', 'released.current.txt'), 'instance-store'),
    (get_image_data('xenial', 'daily.current.txt'), 'instance-store'),
    (get_image_data('xenial', 'released.current.txt'), 'ebs-ssd'),
    (get_image_data('xenial', 'daily.current.txt'), 'ebs-ssd')
])
def test_image_map(image_data, instance_type):
    image_map = get_image_map(image_data, instance_type)
    assert type(image_map) == dict
    assert test_region in image_map
