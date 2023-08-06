#!/usr/bin/env python

"""
setup.py file for Pybind11 C++/Python example
"""
from setuptools import setup, Extension, find_packages


setup (name = 'pybind11_example',
       version = '0.3',
       author      = "zc",
       author_email = "hliu2@thorlabs.com",
       url = "http://www.thorlabs.com",
       description = """Simple Pybind11 C++/Python example""",
       ext_modules = [Extension('pybind11_example',
                           sources=['pybind11_wrapper.cpp'],
                           )
                      ],
       py_modules = ["pybind11_example"],
       packages=find_packages(),
       include_package_data = True,
       )