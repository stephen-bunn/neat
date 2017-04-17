#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

from distutils.core import setup

setup(
    name='NEAT',
    version='0.0.0',
    description='Networked Energy Appliance Translator',
    author='Stephen Bunn',
    author_email='stephen@bunn.io',
    packages=[
        'neat',
        'neat.requester', 'neat.scheduler', 'neat.translator'
    ]
)
