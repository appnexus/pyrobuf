import os
import sys
import pytest

from distutils.util import get_platform


@pytest.fixture(scope='session')
def proto_lib():
    here = os.path.dirname(os.path.abspath(__file__))
    build = os.path.join(here, 'build')
    lib_path = os.path.join(build, "lib.{0}-{1}".format(get_platform(), sys.version[0:3]))

    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)

    return lib_path
