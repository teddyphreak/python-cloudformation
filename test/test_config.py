from nephelaiio.cloudformation import config


def test_config_dummy():
    assert config['DEFAULT']['default'] == 'yes'
