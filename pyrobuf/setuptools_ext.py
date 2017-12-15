"""Setuptools integration."""
import glob
import os
import os.path

from Cython.Build import cythonize
from jinja2 import Environment, PackageLoader
from pyrobuf.__main__ import generate, HERE
from pyrobuf.parse_proto import Parser

try:
    basestring
except NameError:
    # Python 3.x
    basestring = str


def add_pyrobuf_module(dist, pyrobuf_module):
    parser = Parser()

    env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))
    templ_pxd = env.get_template('proto_pxd.tmpl')
    templ_pyx = env.get_template('proto_pyx.tmpl')
    generated = set()
    pyx_files = []

    dir_name = "pyrobuf/_" + pyrobuf_module

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if os.path.isdir(pyrobuf_module):
        for spec in glob.glob(os.path.join(pyrobuf_module, '*.proto')):
            generate(spec, dir_name, parser, templ_pxd, templ_pyx, generated, pyx_files)

        _, name = os.path.split(pyrobuf_module)

    else:
        name, _ = os.path.splitext(os.path.basename(pyrobuf_module))
        if not name:
            print("not a .proto file")
            return

        generate(pyrobuf_module, dir_name, parser, templ_pxd, templ_pyx, generated, pyx_files)

    if dist.ext_modules is None:
        dist.ext_modules = []
    dist.ext_modules.extend(cythonize(pyx_files,
                            include_path=[os.path.join(HERE, 'src'), dir_name]))


def pyrobuf_modules(dist, attr, value):
    assert attr == 'pyrobuf_modules'
    if isinstance(value, basestring):
        value = [value]

    for pyrobuf_module in value:
        add_pyrobuf_module(dist, pyrobuf_module)
