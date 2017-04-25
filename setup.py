#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

from setuptools import (setup, find_packages)

from neat import const


setup(
    name=const.module_name,
    version=const.version,
    description='Networked Energy Appliance Translator',
    long_description='README.md',
    license='GNU GPLv3',
    author='Stephen Bunn',
    author_email='stephen@bunn.io',
    url='https://github.com/ritashugisha/neat',
    platforms='Unix',
    include_package_data=True,
    install_requires=[
        'jsonschema>=2.6.0',
        'requests>=2.13.0',
        'blinker>=1.4',
        'pint>=0.7.2',
        'lxml>=3.4.2',
        'beautifulsoup4>=4.5.3',
        'python-dateutil>=2.6.0',
        'pyyaml>=3.12',
        'rethinkdb>=2.3.0.post6',
        'pymongo>=3.4.0'
    ],
    packages=[
        'neat', 'neat.models', 'neat.requester', 'neat.scheduler',
        'neat.translator', 'neat.pipe'
    ]
)
