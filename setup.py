import os
import sys
import distutils.log

from setuptools import setup, find_packages, Command
from setuptools.command.install import install as _install
from jinja2 import Environment, PackageLoader
from Cython.Build import cythonize


VERSION = "0.5.4"
HERE = os.path.dirname(os.path.abspath(__file__))


class GenerateList(Command):

    description = "generate pyrobuf_list pxd and pyd (for development)"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        self.execute(_pre_install, (self, ), msg="Running pre install task")

class ListAndUtil(Command):

    description = "compile and install pyrobuf_list and pyrobuf_util (for development)"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        self.execute(_post_install, (self, ), msg="Running post install task")

class install(_install):

    def run(self):
        self.execute(_pre_install, (self, ), msg="Running pre install task")
        _install.run(self)
        self.execute(_post_install, (self, ), msg="Running post install task")

def _post_install(command):
    command.announce('Building & installing pyrobuf_util and pyrobuf_list', level=distutils.log.INFO)
    setup(name="pyrobuf_list_and_util",
          version=VERSION,
          ext_modules=cythonize([os.path.join(HERE, 'pyrobuf', 'src', '*.pyx')],
                                include_path=[os.path.join(HERE, 'pyrobuf', 'src')]),
          script_args=['build', 'install'])

def _pre_install(command):
    env = Environment(loader=PackageLoader('pyrobuf.protobuf', 'templates'))

    name_pyx = 'pyrobuf_list.pyx'
    name_pxd = 'pyrobuf_list.pxd'

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

    path = os.path.join(HERE, 'pyrobuf', 'src', name_pyx)
    command.announce('    Generating {0}'.format(path), level=distutils.log.INFO)
    with open(path, 'w') as fp:
        fp.write(templ_pyx.render({'def': listdict, 'version_major': sys.version_info.major}))

    path = os.path.join(HERE, 'pyrobuf', 'src', name_pxd)
    command.announce('    Generating {0}'.format(path), level=distutils.log.INFO)
    with open(path, 'w') as fp:
        fp.write(templ_pxd.render({'def': listdict, 'version_major': sys.version_info.major}))


setup(
    name="pyrobuf",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'install': install,
              'generate_list': GenerateList,
              'list_and_util': ListAndUtil},
    entry_points={
        'console_scripts': ['pyrobuf = pyrobuf.__main__:main']
    },
    description='A Cython based protobuf compiler',
    long_description=open(os.path.join(HERE, 'README.md')).read(),
    url='https://github.com/appnexus/pyrobuf',
    author='AppNexus',
)
