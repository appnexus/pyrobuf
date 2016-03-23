"""Setuptools integration."""
import glob
import os

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

    dir_name = "pyrobuf/_" + pyrobuf_module

    os.makedirs(dir_name, exist_ok=True)

    if os.path.isdir(pyrobuf_module):
        for spec in glob.glob(os.path.join(pyrobuf_module, '*.proto')):
            generate(spec, dir_name, parser, templ_pxd, templ_pyx)

        _, name = os.path.split(pyrobuf_module)
        pyx = os.path.join(dir_name, '*.pyx')

    else:
        name, _ = os.path.splitext(os.path.basename(pyrobuf_module))
        if not name:
            print("not a .proto file")
            return

        generate(pyrobuf_module, dir_name, parser, templ_pxd, templ_pyx)

        pyx = os.path.join(dir_name, "%s_proto.pyx" % name)

    if dist.ext_modules is None:
        dist.ext_modules = []
    dist.ext_modules.extend(cythonize([pyx],
                            include_path=[os.path.join(HERE, 'src'), dir_name]))


def pyrobuf_modules(dist, attr, value):
    assert attr == 'pyrobuf_modules'
    if isinstance(value, basestring):
        value = [value]

    for pyrobuf_module in value:
        add_pyrobuf_module(dist, pyrobuf_module)
