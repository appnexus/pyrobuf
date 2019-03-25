from distutils.command.clean import clean as _clean
from distutils.dir_util import remove_tree
from distutils import log

from setuptools import setup, find_packages, Distribution

import os
import os.path
import platform
import sys


VERSION = "0.8.7"
HERE = os.path.dirname(os.path.abspath(__file__))
PYROBUF_DEFS_PXI = "pyrobuf_defs.pxi"
PYROBUF_LIST_PXD = "pyrobuf_list.pxd"
PYROBUF_LIST_PYX = "pyrobuf_list.pyx"


class clean(_clean):
    def __clean_tree(self, tree):
        for dirpath, dirnames, filenames in os.walk(tree):
            for dirname in dirnames:
                if dirname in ('__pycache__', 'build'):
                    remove_tree(os.path.join(dirpath, dirname), verbose=self.verbose, dry_run=self.dry_run)

        for dirpath, dirnames, filenames in os.walk(tree):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in (".so", ".pyd", ".dll", ".pyc")):
                    self.__remove_file(os.path.join(dirpath, filename))
                    continue
                extension = os.path.splitext(filename)[1]
                if extension in ['.c', '.h']:
                    pyx_file = str.replace(filename, extension, '.pyx')
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        self.__remove_file(os.path.join(dirpath, filename))

    def __remove_file(self, full_path):
        if os.path.exists(full_path):
            if not self.dry_run:
                os.unlink(full_path)
            if self.verbose >= 1:
                log.info("removing '%s'" % full_path)

    def run(self):
        _clean.run(self)

        self.__clean_tree(os.path.join(HERE, 'pyrobuf'))
        self.__clean_tree(os.path.join(HERE, 'tests'))

        tests_out = os.path.join(HERE, 'tests', 'out')
        if os.path.isdir(tests_out):
            remove_tree(tests_out, verbose=self.verbose, dry_run=self.dry_run)

        self.__remove_file(os.path.join(HERE, 'pyrobuf', 'src', PYROBUF_DEFS_PXI))
        self.__remove_file(os.path.join(HERE, 'pyrobuf', 'src', PYROBUF_LIST_PXD))
        self.__remove_file(os.path.join(HERE, 'pyrobuf', 'src', PYROBUF_LIST_PYX))

        for filename in os.listdir(HERE):
            for prefix in ("pyrobuf_list", "pyrobuf_util"):
                for suffix in (".so", ".pyd"):
                    if filename.startswith(prefix) and filename.endswith(suffix):
                        self.__remove_file(os.path.join(HERE, filename))


class PyrobufDistribution(Distribution):

    def run_commands(self):
        # By now the setup_requires deps have been fetched.
        if not self.ext_modules:
            self.ext_modules = list()
        self.ext_modules.extend(self.pyrobufize_builtins())
        Distribution.run_commands(self)

    def pyrobufize_builtins(self):
        from jinja2 import Environment, PackageLoader
        from Cython.Build import cythonize
        env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))

        templ_pyx = env.get_template('pyrobuf_list_pyx.tmpl')
        templ_pxd = env.get_template('pyrobuf_list_pxd.tmpl')

        listdict = {
            'DoubleList':   'double',
            'FloatList':    'float',
            'IntList':      'int',
            'Int32List':    'int32_t',
            'Uint32List':   'uint32_t',
            'Int64List':    'int64_t',
            'Uint64List':   'uint64_t',
            'CharList':     'char'
        }

        format_map = {
            'double': 'd',
            'float': 'f',
            'int': 'i',
            'int32_t': 'i',
            'uint32_t': 'I',
            'int64_t': 'L',
            'uint64_t': 'K',
            'char': 'c',
        }

        # Even if PYROBUF_LIST_PYX and PYROBUF_LIST_PXD already exist they should be re-built because
        # we don't know whether they were built using *this* version of Python.
        path = os.path.join(HERE, 'pyrobuf', 'src', PYROBUF_LIST_PYX)
        if not self.dry_run:
            with open(path, 'w') as fp:
                fp.write(templ_pyx.render(
                    {'def': listdict, 'version_major': sys.version_info.major, 'format_map': format_map}
                ))
        if self.verbose >= 1:
            log.info("rendering '%s' from '%s'" % (PYROBUF_LIST_PYX, templ_pyx.filename))

        path = os.path.join(HERE, 'pyrobuf', 'src', PYROBUF_LIST_PXD)
        if not self.dry_run:
            with open(path, 'w') as fp:
                fp.write(templ_pxd.render(
                    {'def': listdict, 'version_major': sys.version_info.major, 'format_map': format_map}
                ))
        if self.verbose >= 1:
            log.info("rendering '%s' from '%s'" % (PYROBUF_LIST_PXD, templ_pxd.filename))

        # Cython doesn't always supply the UNAME_SYSNAME definition, so we'll roll our own
        path = os.path.join(HERE, 'pyrobuf', 'src', PYROBUF_DEFS_PXI)
        with open(path, 'w') as defs:
            uname = zip(('SYSNAME', 'NODENAME', 'RELEASE', 'VERSION', 'MACHINE'), platform.uname())
            defs.write("# Generated by pyrobuf/setup.py. DO NOT EDIT!\n\n")
            defs.write('\n'.join('DEF PYROBUF_UNAME_%s = "%s"' % (k, v) for k, v in uname))
            defs.write('\n')

        return cythonize(['pyrobuf/src/*.pyx'],
                         include_path=['pyrobuf/src'])


setup(
    distclass=PyrobufDistribution,
    name="pyrobuf",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'clean': clean},
    entry_points={
        'console_scripts': ['pyrobuf = pyrobuf.__main__:main'],
        'distutils.setup_keywords': [
            'pyrobuf_modules = pyrobuf.setuptools_ext:pyrobuf_modules',
        ],
    },
    description='A Cython based protobuf compiler',
    long_description=open(os.path.join(HERE, 'README.md')).read(),
    url='https://github.com/appnexus/pyrobuf',
    author='AppNexus',
    tests_require=['pytest'] + (['protobuf >= 2.6.0, <3'] if sys.version_info.major == 2 else []),
    setup_requires=['jinja2 >= 2.8', 'cython >= 0.23', 'pytest-runner'],
    install_requires=['jinja2 >= 2.8', 'cython >= 0.23'],
    zip_safe=False,
)
