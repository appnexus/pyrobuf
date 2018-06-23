"""Setuptools integration."""
import os
import os.path

from Cython.Build import cythonize
from pyrobuf.__main__ import compile_spec, HERE

try:
    basestring
except NameError:
    # Python 3.x
    basestring = str


def add_pyrobuf_module(dist, pyrobuf_module):
    dir_name = "pyrobuf/_" + pyrobuf_module
    pyx_files = compile_spec(pyrobuf_module, out=dir_name)
    include_path = [os.path.join(HERE, 'src'), dir_name]

    if dist.ext_modules is None:
        dist.ext_modules = []

    dist.ext_modules.extend(cythonize(pyx_files, include_path=include_path))


def pyrobuf_modules(dist, attr, value):
    assert attr == 'pyrobuf_modules'
    if isinstance(value, basestring):
        value = [value]

    for pyrobuf_module in value:
        add_pyrobuf_module(dist, pyrobuf_module)
