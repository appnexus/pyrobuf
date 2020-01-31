"""Setuptools integration."""
import os
import sys

from pyrobuf.compile import Compiler

if sys.version_info.major == 3:
    basestring = str
    _FileExistsError = FileExistsError
else:
    _FileExistsError = OSError


def add_pyrobuf_module(dist, pyrobuf_module):
    dir_name = "pyrobuf/_" + pyrobuf_module
    package = "{}_{}".format(dist.get_name(), pyrobuf_module)
    try:
        os.makedirs(os.path.join(dir_name, package))
    except _FileExistsError:
        pass
    compiler = Compiler([pyrobuf_module], out=dir_name, package=package)
    compiler.extend(dist)


def pyrobuf_modules(dist, attr, value):
    assert attr == 'pyrobuf_modules'
    if isinstance(value, basestring):
        value = [value]

    for pyrobuf_module in value:
        add_pyrobuf_module(dist, pyrobuf_module)
