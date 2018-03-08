import os
import sys
import glob
import argparse
from setuptools import setup

from Cython.Build import cythonize
from jinja2 import Environment, PackageLoader

from pyrobuf.parse_proto import Parser
from pyrobuf.parse_proto3 import Proto3Parser


HERE = os.path.dirname(os.path.abspath(__file__))

if sys.version_info.major == 3:
    _FileExistsError = FileExistsError
else:
    _FileExistsError = OSError


def main():
    args = cli_argument_parser()
    gen_message(args.source, out=args.out_dir, build=args.build_dir,
                install=args.install, proto3=args.proto3, force=args.force)


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
    parser.add_argument('--proto3', action='store_true',
                        help="compile proto3 syntax [default: False]")
    parser.add_argument('--force', action='store_true',
                        help="force install")
    return parser.parse_args()


def gen_message(fname, out="out", build="build", install=False, proto3=False,
                force=False):

    if proto3:
        parser = Proto3Parser()
    else:
        parser = Parser()

    env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))
    templ_pxd = env.get_template('proto_pxd.tmpl')
    templ_pyx = env.get_template('proto_pyx.tmpl')
    generated = set()
    pyx_files = []

    try:
        os.makedirs(out)
    except _FileExistsError:
        pass

    script_args = ['build', '--build-base={0}'.format(build)]
    if install:
        script_args.append('install')

    if force:
        script_args.append('--force')

    if os.path.isdir(fname):
        for spec in glob.glob(os.path.join(fname, '*.proto')):
            generate(spec, out, parser, templ_pxd, templ_pyx, generated,
                     pyx_files)

        _, name = os.path.split(fname)

    else:
        name, _ = os.path.splitext(os.path.basename(fname))
        if not name:
            print("not a .proto file")
            return

        generate(fname, out, parser, templ_pxd, templ_pyx, generated, pyx_files)

    setup(name=name,
          ext_modules=cythonize(pyx_files,
                                include_path=[os.path.join(HERE, 'src'), out]),
          script_args=script_args)


def generate(fname, out, parser, templ_pxd, templ_pyx, generated, pyx_files):
    name, _ = os.path.splitext(os.path.basename(fname))
    directory = os.path.dirname(fname)

    if name in generated:
        return

    print("generating {0}".format(fname))
    generated.add(name)

    name_pxd = "%s_proto.pxd" % name
    name_pyx = "%s_proto.pyx" % name
    pyx_files.append(os.path.join(out, name_pyx))

    msgdef = parser.parse_from_filename(fname)

    with open(os.path.join(out, name_pxd), 'w') as fp:
        fp.write(templ_pxd.render(msgdef, version_major=sys.version_info.major))

    with open(os.path.join(out, name_pyx), 'w') as fp:
        fp.write(templ_pyx.render(msgdef, version_major=sys.version_info.major))

    for f in msgdef['imports']:
        print("parsing dependency '{}'".format(f))
        try:
            generate(os.path.join(directory, '{}.proto'.format(f)),
                     out, parser, templ_pxd, templ_pyx, generated, pyx_files)
        except FileNotFoundError:
            print("can't find message spec for '{}'".format(f))


if __name__ == "__main__":
    main()
