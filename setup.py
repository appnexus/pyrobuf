from setuptools import setup, find_packages
from setuptools.command.install import install as _install

import os
import sys


VERSION = "0.5.5"
HERE = os.path.dirname(os.path.abspath(__file__))


class install(_install):
    def run(self):
        # By now the setup_requires deps have been fetched.
        self.distribution.ext_modules = self.pyrobufize_builtins()
        super(_install, self).run()

    @staticmethod
    def pyrobufize_builtins():
        from jinja2 import Environment, PackageLoader
        from Cython.Build import cythonize
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
        with open(path, 'w') as fp:
            fp.write(templ_pyx.render({'def': listdict, 'version_major': sys.version_info.major}))

        path = os.path.join(HERE, 'pyrobuf', 'src', name_pxd)
        with open(path, 'w') as fp:
            fp.write(templ_pxd.render({'def': listdict, 'version_major': sys.version_info.major}))

        return cythonize(['pyrobuf/src/*.pyx'],
                         include_path=['pyrobuf/src'])


setup(
    name="pyrobuf",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'install': install},
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
    setup_requires=['jinja2', 'cython >= 0.23'],
    install_requires=['jinja2', 'cython >= 0.23'],
)
