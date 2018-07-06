import argparse
import glob
import os
import sys
from setuptools import setup

from Cython.Build import cythonize
from jinja2 import Environment, PackageLoader

from pyrobuf.parse_proto import Parser, Proto3Parser

if sys.version_info.major == 3:
    _FileExistsError = FileExistsError
else:
    _FileExistsError = OSError

_VM = sys.version_info.major


class Compiler(object):

    _env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))
    t_pxd = _env.get_template('proto_pxd.tmpl')
    t_pyx = _env.get_template('proto_pyx.tmpl')

    def __init__(self, source, out="out", build="build", install=False,
                 proto3=False, force=False, package=None):
        self.source = source
        self.out = out
        self.build = build
        self.install = install
        self.force = force
        self.package = package
        here = os.path.dirname(os.path.abspath(__file__))
        self.include_path = [os.path.join(here, 'src'), self.out]
        self._generated = set()
        self._messages = []
        self._pyx_files = []

        if proto3:
            self.parser = Proto3Parser
        else:
            self.parser = Parser

    @classmethod
    def parse_cli_args(cls):
        parser = argparse.ArgumentParser(
            "pyrobuf", description="a Cython based protobuf compiler")
        parser.add_argument('source', type=str,
                            help="<filename>.proto or directory containing "
                                 "proto files")
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
        args = parser.parse_args()

        return cls(args.source, out=args.out_dir, build=args.build_dir,
                   install=args.install, proto3=args.proto3, force=args.force,
                   package=args.package)

    def compile(self):
        script_args = ['build', '--build-base={0}'.format(self.build)]

        if self.install:
            script_args.append('install')

        if self.force:
            script_args.append('--force')

        self._compile_spec()

        if self.package is not None:
            self._package()

        setup(name='pyrobuf-generated',
              ext_modules=cythonize(self._pyx_files,
                                    include_path=self.include_path),
              script_args=script_args)

    def extend(self, dist):
        self._compile_spec()

        if self.package is not None:
            self._package()

        if dist.ext_modules is None:
            dist.ext_modules = []

        dist.ext_modules.extend(cythonize(self._pyx_files,
                                          include_path=self.include_path))

    def _compile_spec(self):
        try:
            os.makedirs(self.out)
        except _FileExistsError:
            pass

        if os.path.isdir(self.source):
            for spec in glob.glob(os.path.join(self.source, '*.proto')):
                self._generate(spec)
        else:
            self._generate(self.source)

    def _generate(self, filename):
        name, _ = os.path.splitext(os.path.basename(filename))
        directory = os.path.dirname(filename)

        if name in self._generated:
            return

        print("generating {0}".format(filename))
        self._generated.add(name)

        msg_def = self.parser.parse_from_filename(filename)
        self._messages.append(msg_def)

        for f in msg_def['imports']:
            print("parsing dependency '{}'".format(f))
            try:
                self._generate(os.path.join(directory, '{}.proto'.format(f)))
            except FileNotFoundError:
                raise FileNotFoundError("can't find message spec for '{}'"
                                        .format(f))

        if self.package is None:
            self._write(name, msg_def)

    def _write(self, name, msg_def):
        name_pxd = "{}_proto.pxd".format(name)
        name_pyx = "{}_proto.pyx".format(name)
        self._pyx_files.append(os.path.join(self.out, name_pyx))

        with open(os.path.join(self.out, name_pxd), 'w') as fp:
            fp.write(self.t_pxd.render(msg_def, version_major=_VM))

        with open(os.path.join(self.out, name_pyx), 'w') as fp:
            fp.write(self.t_pyx.render(msg_def, version_major=_VM))

    def _package(self):
        meta = {'imports': [], 'messages': [], 'enums': []}

        for msg_def in self._messages:
            meta['messages'].extend(msg_def['messages'])
            meta['enums'].extend(msg_def['enums'])

        name_pxd = "{}.pxd".format(self.package)
        name_pyx = "{}.pyx".format(self.package)
        self._pyx_files.append(os.path.join(self.out, name_pyx))

        with open(os.path.join(self.out, name_pxd), 'w') as fp:
            fp.write(self.t_pxd.render(meta, version_major=_VM))

        with open(os.path.join(self.out, name_pyx), 'w') as fp:
            fp.write(self.t_pyx.render(meta, version_major=_VM))
