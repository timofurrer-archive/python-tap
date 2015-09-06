#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import load_source
from distutils.core import setup

core = load_source("core", "tap/__init__.py")

setup(
    name="tap",
    version=core.__version__,
    license="GPLv2",
    description="Pythonic module to produce TAP (Test Anything Protocol) result files",
    author=core.__author__,
    author_email=core.__email__,
    maintainer=core.__author__,
    maintainer_email=core.__email__,
    platforms=["Linux"],
    url="http://github.com/timofurrer/python-tap",
    download_url="http://github.com/timofurrer/python-tap",
    packages=["tap"]
)
