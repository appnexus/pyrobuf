from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(["src/*.pyx", "out/*_proto.pyx"],
                            include_path=["out", "src"]))
