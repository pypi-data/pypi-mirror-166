from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    name="unthrow",
    version="0.1",
    description="An exception that can be resumed. ",
    author="Joe Marshall",
    author_email="joe.marshall@nottingham.ac.uk",
    url="https://github.com/joemarshall/unthrow",
    py_modules=["unthrow"],
    install_requires=['cython'],
    ext_modules = cythonize("unthrow/*.pyx")
)
