import os
import sys
import distutils.log

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from jinja2 import Environment, PackageLoader
from Cython.Build import cythonize


VERSION = "0.0.1"
HERE = os.path.dirname(os.path.abspath(__file__))

class install(_install):
    def run(self):
        self.execute(self._pre_install, (), msg="Running pre install task")
        _install.run(self)
        self.execute(self._post_install, (), msg="Running post install task")

    def _pre_install(self):
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
        self.announce('    Generating {0}'.format(path), level=distutils.log.INFO)
        with open(path, 'w') as fp:
            fp.write(templ_pyx.render({'def': listdict, 'version_major': sys.version_info.major}))

        path = os.path.join(HERE, 'pyrobuf', 'src', name_pxd)
        self.announce('    Generating {0}'.format(path), level=distutils.log.INFO)
        with open(path, 'w') as fp:
            fp.write(templ_pxd.render({'def': listdict, 'version_major': sys.version_info.major}))

    def _post_install(self):
        self.announce('Building & installing pyrobuf_util and pyrobuf_list', level=distutils.log.INFO)
        setup(name="pyrobuf_postinstall",
              version=VERSION,
              ext_modules=cythonize([os.path.join(HERE, 'pyrobuf', 'src', '*.pyx')],
                                    include_path=[os.path.join(HERE, 'pyrobuf', 'src')]),
              script_args=['build', 'install'])

setup(
    name="pyrobuf",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'install': install},
    entry_points={
        'console_scripts': ['pyrobuf = pyrobuf.__main__:main']
    }
)
