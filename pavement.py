from paver.easy import *
import pytest

@task
def test():
    pytest.main(['-s'])
