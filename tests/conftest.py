import os
import sys

from distutils.util import get_platform
from pyrobuf.compile import Compiler


def pytest_sessionstart(session):
    # Build test messages from proto specs
    here = os.path.dirname(os.path.abspath(__file__))
    proto = [os.path.join(here, 'proto', filename)
             for filename in os.listdir(os.path.join(here, 'proto'))]
    compiler = Compiler(proto, out='tests/out', build='tests/build')
    compiler.compile()

    # Add test directory into path
    if here not in sys.path:
        sys.path.append(here)

    # Insert built messages into path
    build = os.path.join(here, 'build')
    lib_path = os.path.join(build, "lib.{0}-{1}".format(get_platform(),
                                                        sys.version[0:3]))

    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)
