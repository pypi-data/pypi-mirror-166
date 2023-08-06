#!/usr/bin/env python

"""
setup.py file for SWIG C++/Python example
"""
from setuptools import setup, Extension, find_packages

setup (name = 'exampleSWIG',
       version='0.1',
       author="zc",
       author_email="hliu2@thorlabs.com",
       url="https://www.thorlabs.com",
       description = """Simple swig C++/Python example""",
       ext_modules = [Extension('_exampleSWIG',
                           sources=['example.cpp', 'example_wrap.cxx',],
                           )
                      ],
       py_modules = ["exampleSWIG"],
       packages=find_packages(),
       include_package_data = True,
       zip_safe = False
       )
