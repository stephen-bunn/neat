#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
client.py
.. module:: modman
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-24-2017 10:34:23
    :modified: 02-24-2017 10:34:23
.. moduleauthor:: Stephen Bunn <r>
"""

import os

from . import const
from .engine import Engine
from . import (
    scheduler,
    requester,
    pipe
)

import yaml


class Client(object):

    def __init__(self, config: dict):
        device_pairs = []
        for device in config:
            device_scheduler = getattr(scheduler, device['scheduler']['$'])(**{
                k: v
                for (k, v) in device['scheduler'].items()
                if k != '$'
            })
            device_requester = getattr(requester, device['requester']['$'])(**{
                k: v
                for (k, v) in device['requester'].items()
                if k != '$'
            })
            device_pairs.append((device_scheduler, device_requester))
        self.engine = Engine(dict(device_pairs), [
            pipe.RethinkDBPipe('localhost', 28015, 'devices')
        ])

    @staticmethod
    def from_config(config: str):
        config = os.path.abspath(os.path.expanduser(config))
        if os.path.isfile(config):
            with open(config, 'r') as fp:
                try:
                    return Client(yaml.load(fp))
                except yaml.YAMLError as exc:
                    const.log.error((
                        'client failed loading from config at `{config}`, '
                        '{exc.message} ...'
                    ).format(config=config, exc=exc))
        else:
            raise FileNotFoundError((
                "given file at '{config}' does not exist"
            ).format(config=config))

    def start(self) -> None:
        try:
            self.engine.start()
            for _ in self.engine.register.keys():
                _.join()
        except KeyboardInterrupt:
            const.log.info(('terminating client `{self}`').format(self=self))
            self.engine.stop()
