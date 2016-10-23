from .images.ubuntu import get_release_image_map
from .base import base_template
from . import config


def ubuntu(release, fn):
    template = base_template(fn)
    template.add_mapping(config['regionmap']['name'], get_release_image_map(release))
    return template

