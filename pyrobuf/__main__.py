import os
import sys
import glob
import argparse
from setuptools import setup

from Cython.Build import cythonize
from jinja2 import Environment, PackageLoader

from pyrobuf.parse_proto import Parser, Proto3Parser


HERE = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))
T_PXD = env.get_template('proto_pxd.tmpl')
T_PYX = env.get_template('proto_pyx.tmpl')

if sys.version_info.major == 3:
    _FileExistsError = FileExistsError
else:
    _FileExistsError = OSError


def main():
    args = cli_argument_parser()
    gen_message(args.source, out=args.out_dir, build=args.build_dir,
                install=args.install, proto3=args.proto3, force=args.force,
                package=args.package)


def cli_argument_parser():
    parser = argparse.ArgumentParser(
        "pyrobuf", description="a Cython based protobuf compiler")
    parser.add_argument('source', type=str,
                        help="<filename>.proto or directory containing proto "
                             "files")
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
    parser.add_argument('--package', type=str, default=None,
                        help="name of package to compile to")
    return parser.parse_args()


def gen_message(fname, out="out", build="build", install=False, proto3=False,
                force=False, package=None):
    script_args = ['build', '--build-base={0}'.format(build)]

    if install:
        script_args.append('install')

    if force:
        script_args.append('--force')

    pyx_files, includes = compile_spec(fname, out=out, proto3=proto3)
    include_path = [os.path.join(HERE, 'src'), out]

    if package is not None:
        agg_file = os.path.join(out, '{}.pyx'.format(package))
        with open(agg_file, 'w') as fp:
            for name in includes:
                fp.write('include "{}"\n'.format(name))

        pyx_files = agg_file

    setup(name='pyrobuf-generated',
          ext_modules=cythonize(pyx_files, include_path=include_path),
          script_args=script_args)


def compile_spec(fname, out="out", proto3=False):
    if proto3:
        parser = Proto3Parser
    else:
        parser = Parser

    generated = set()
    pyx_files = []
    includes = []

    try:
        os.makedirs(out)
    except _FileExistsError:
        pass

    if os.path.isdir(fname):
        for spec in glob.glob(os.path.join(fname, '*.proto')):
            generate(spec, out, parser, generated, pyx_files, includes)
    else:
        generate(fname, out, parser, generated, pyx_files, includes)

    return pyx_files, includes


def generate(fname, out, parser, generated, pyx_files, includes):
    name, _ = os.path.splitext(os.path.basename(fname))
    directory = os.path.dirname(fname)

    if name in generated:
        return

    print("generating {0}".format(fname))
    generated.add(name)

    name_pxd = "%s_proto.pxd" % name
    name_pyx = "%s_proto.pyx" % name
    pyx_files.append(os.path.join(out, name_pyx))
    includes.append(name_pyx)
    msgdef = parser.parse_from_filename(fname)

    with open(os.path.join(out, name_pxd), 'w') as fp:
        fp.write(T_PXD.render(msgdef, version_major=sys.version_info.major))

    with open(os.path.join(out, name_pyx), 'w') as fp:
        fp.write(T_PYX.render(msgdef, version_major=sys.version_info.major))

    for f in msgdef['imports']:
        print("parsing dependency '{}'".format(f))
        try:
            generate(os.path.join(directory, '{}.proto'.format(f)),
                     out, parser, generated, pyx_files, includes)
        except FileNotFoundError:
            raise FileNotFoundError("can't find message spec for '{}'"
                                    .format(f))


if __name__ == "__main__":
    main()
