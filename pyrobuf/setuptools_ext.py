"""Setuptools integration."""
from pyrobuf.compile import Compiler

try:
    basestring
except NameError:
    # Python 3.x
    basestring = str


def add_pyrobuf_module(dist, pyrobuf_module):
    dir_name = "pyrobuf/_" + pyrobuf_module
    compiler = Compiler(pyrobuf_module, out=dir_name,
                        package="{}_{}".format(dist.get_name(), pyrobuf_module))
    compiler.extend(dist)


def pyrobuf_modules(dist, attr, value):
    assert attr == 'pyrobuf_modules'
    if isinstance(value, basestring):
        value = [value]

    for pyrobuf_module in value:
        add_pyrobuf_module(dist, pyrobuf_module)
