# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="py-base-layer",
    version='1.0.0',
    author="ThinkTik",
    author_email="thinktik@outlook.com",
    description="AWS lambda python runtime base layer libs",
    long_description="这个是omoz.cc管理的运行在AWS lambda python runtime上的第三方基础依赖库集合",
    url="https://www.omoz.cc",
    packages=find_packages(where="."),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': [''],
    },
    platforms=["linux", "windows"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
