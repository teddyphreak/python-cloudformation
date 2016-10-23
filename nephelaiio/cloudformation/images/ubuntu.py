import urllib.request
from functools import reduce


def get_image_data(release, source='released.current.txt', timeout=5):
    """
    Query ubuntu cloud image lists for data

    :param release: The ubuntu release to query
    :param source: the url query prefix. Must be one of the base names listed at
    https://cloud-images.ubuntu.com/query/xenial/server/
    :param timeout: The query timeout in seconds
    :return: The raw image data as
    """
    cloud_images_url = "https://cloud-images.ubuntu.com/query/{0}/server/{1}".format(release, source)
    with urllib.request.urlopen(cloud_images_url, timeout=timeout) as response:
        return response.read().decode().splitlines()


def get_image_map(image_data, instance_type='instance-store'):
    """
    Build EC2 region to AMI map table

    :param image_data: The raw image data as returned from get_image_data
    :param instance_type: The instance type to include in the map. One of ['instance-store', 'ebs-ssd']
    :return: dictionary associating ec2 regions with corresponding ubuntu ami. I.e.
    { 'ap-northeast-1': {'ami': 'ami-71b81e10'} }
    """
    image_data = filter(lambda x: len(x.split()) > 7, image_data)
    image_map = [dict(zip(['instance_type', 'region', 'ami'],
                          [x.split()[4], x.split()[6], x.split()[7]]))
                 for x in image_data]
    image_map = [dict(zip(['region', 'ami'], [z['region'], z['ami']]))
                 for z in image_map if z['instance_type'] == instance_type]
    image_map = reduce(lambda x, y: {**x, **{y['region']: {'ami': y['ami']}}}, [{}] + image_map)
    return image_map


def get_daily_image_map(release, source='daily.current.txt', timeout=5, instance_type='instance-store'):
    """
    Helper method to retrieve latest ubuntu daily image map

    :param release: The ubuntu release to query
    :param source: the url query prefix. Must be one of the base names listed at
    https://cloud-images.ubuntu.com/query/xenial/server/
    :param timeout: The query timeout in seconds
    :param instance_type: The instance type to include in the map. One of ['instance-store', 'ebs-ssd']
    :return: dictionary associating ec2 regions with corresponding ubuntu ami. I.e.
    { 'ap-northeast-1': {'ami': 'ami-71b81e10'} }
    """
    image_data = get_image_data(release, source, timeout)
    return get_image_map(image_data, instance_type)


def get_release_image_map(release, source='released.current.txt', timeout=5, instance_type='instance-store'):
    """
    Helper method to retrieve latest ubuntu release image map

    :param release: The ubuntu release to query
    :param source: the url query prefix. Must be one of the base names listed at
    https://cloud-images.ubuntu.com/query/xenial/server/
    :param timeout: The query timeout in seconds
    :param instance_type: The instance type to include in the map. One of ['instance-store', 'ebs-ssd']
    :return: dictionary associating ec2 regions with corresponding ubuntu ami. I.e.
    { 'ap-northeast-1': {'ami': 'ami-71b81e10'} }
    """
    image_data = get_image_data(release, source, timeout)
    return get_image_map(image_data, instance_type)
