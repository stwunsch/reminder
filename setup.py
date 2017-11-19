#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name="reminder",
    version="0.0.1",
    author="Stefan Wunsch",
    author_email="foo@bar.com",
    description=
    ("Tiny command-line app to remind yourself what your former self wanted to do."
     ),
    license="GPL v3",
    keywords="reminder",
    packages=["reminder"],
    classifiers=["Development Status :: 3 - Alpha", "Topic :: Utilities"],
    scripts=['bin/reminder'])
