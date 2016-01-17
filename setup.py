import os, sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from Cython.Build import cythonize


VERSION = "0.0.1"

def _post_install():
    setup(name="pyrobuf_postinstall",
          version=VERSION,
          ext_modules=cythonize(["src/*.pyx"],
                                include_path=["src"]),
          script_args=['build', 'install'])

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (), msg="Running post install task")

setup(
    name="pyrobuf",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'install': install},
)
