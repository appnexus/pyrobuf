import re
import os
import sys
import glob
import argparse
from distutils.core import setup

from Cython.Build import cythonize
from jinja2 import Environment, PackageLoader

from .parse_proto import Parser


HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    args = cli_argument_parser()
    gen_message(args.source, out=args.out_dir, build=args.build_dir, install=args.install)

def cli_argument_parser():
    parser = argparse.ArgumentParser("pyrobuf", description="a Cython based protobuf compiler")
    parser.add_argument('source', type=str,
                        help="filename.proto or directory containing proto files")
    parser.add_argument('--out-dir', default='out',
                        help="cythonize output directory [default: out]")
    parser.add_argument('--build-dir', default='build',
                        help="C compiler build directory [default: build]")
    parser.add_argument('--install', action='store_true',
                        help="install the extension [default: False]")
    return parser.parse_args()

def gen_message(fname, out="out", build="build", install=False):

    parser = Parser()

    env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))
    templ_pxd = env.get_template('proto_pxd.tmpl')
    templ_pyx = env.get_template('proto_pyx.tmpl')

    try:
        os.makedirs(out)
    except:
        pass

    script_args = ['build', '--build-base={0}'.format(build)]
    if install:
        script_args.append('install')

    if os.path.isdir(fname):
        for spec in glob.glob(os.path.join(fname, '*.proto')):
            generate(spec, out, parser, templ_pxd, templ_pyx)

        _, name = os.path.split(fname)
        pyx = os.path.join(out, '*.pyx')

    else:
        name, _ = os.path.splitext(os.path.basename(fname))
        if not name:
            print("not a .proto file")
            return

        generate(fname, out, parser, templ_pxd, templ_pyx)

        pyx = os.path.join(out, "%s_proto.pyx" % name)

    setup(name=name,
          ext_modules=cythonize([pyx],
                                include_path=[os.path.join(HERE, 'src'), out]),
          script_args=script_args)

def generate(fname, out, parser, templ_pxd, templ_pyx):

    print("generating {0}".format(fname))

    m, _ = os.path.splitext(os.path.basename(fname))

    name_pxd = "%s_proto.pxd" % m
    name_pyx = "%s_proto.pyx" % m

    msgdef = parser.parse_from_filename(fname)

    with open(os.path.join(out, name_pxd), 'w') as fp:
        fp.write(templ_pxd.render(msgdef, version_major=sys.version_info.major))

    with open(os.path.join(out, name_pyx), 'w') as fp:
        fp.write(templ_pyx.render(msgdef, version_major=sys.version_info.major))


if __name__ == "__main__":
    main()
