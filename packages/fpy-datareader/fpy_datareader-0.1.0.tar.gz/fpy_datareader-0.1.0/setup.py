#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FPy DataReader

@author: WeLLiving@well-living
"""

from setuptools import setup, find_packages

setup(
    name="fpy_datareader",
    version="0.1.0",
    description="Remote data access to government data for pandas.",
    author="well-living",
    license="MIT",
    packages=find_packages(),  # "fpy_datareader"
    classfiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["numpy", "pandas", "requests"],
)
