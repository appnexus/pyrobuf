import re
import sys
import os
from distutils.core import setup
import argparse

from jinja2 import Environment, PackageLoader
from Cython.Build import cythonize

from parse_proto import Parser


def gen_message(fname, out="out", build="build", install=False):
    m, _ = os.path.splitext(os.path.basename(fname))
    if m is None:
        print("not a .proto file")
        return

    name_pxd = "%s_proto.pxd" % m
    name_pyx = "%s_proto.pyx" % m

    parser = Parser()
    msgdef = parser.parse_from_filename(fname)

    env = Environment(loader=PackageLoader('protobuf', 'templates'))

    templ_pxd = env.get_template('proto_pxd.tmpl')
    templ_pyx = env.get_template('proto_pyx.tmpl')

    try:
        os.makedirs(out)
    except:
        pass

    with open(os.path.join(out, name_pxd), 'w') as fp:
        fp.write(templ_pxd.render(msgdef))

    with open(os.path.join(out, name_pyx), 'w') as fp:
        fp.write(templ_pyx.render(msgdef))

    script_args = ['build', '--build-base={0}'.format(build)]
    if install:
        script_args.append('install')

    setup(name=m,
          ext_modules=cythonize([os.path.join(out, name_pyx)],
                                include_path=['src']),
          script_args=script_args)


def cli_argument_parser():
    parser = argparse.ArgumentParser("pyrobuf - a Cython base protobuf _compiler_")
    parser.add_argument('source', type=str,
                        help="filename.proto or directory containing proto files")
    parser.add_argument('--out-dir', default='out',
                        help="cythonize output directory [default out]")
    parser.add_argument('--build-dir', default='build',
                        help="C compiler build directory [default build]")
    parser.add_argument('--install', action='store_true',
                        help="install the extension [default False]")
    return parser.parse_args()

if __name__ == "__main__":
    args = cli_argument_parser()
    gen_message(args.source, out=args.out_dir, build=args.build_dir, install=args.install)
