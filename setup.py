from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Plex Synchronizer",
    ext_modules=cythonize("lib/*.py", build_dir="compiled/build"),
    zip_safe=False,
)
