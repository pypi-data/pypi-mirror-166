# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["chico"]

package_data = {"": ["*"]}

install_requires = ["SQLAlchemy>=1.4.40,<2.0.0"]

with open("README.md", "rb") as readme:
    LONG_DESCRIPTION = readme.read().decode()

setup_kwargs = {
    "name": "chico",
    "version": "1.0.0",
    "description": "utils package",
    "long_description": LONG_DESCRIPTION,
    "author": "Hung-Lin, Chen",
    "author_email": "hungln59638@gmail.com",
    "maintainer": "Hung-Lin, Chen",
    "maintainer_email": "hungln59638@gmail.com",
    "url": "https://github.com/hunglin59638/chico",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
