#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import os
import abc

from . import const
from .engine import Engine
from . import (
    scheduler,
    requester,
    pipe
)

import yaml


class AbstractClient(object, metaclass=abc.ABCMeta):
    """ The basic class for all valid clients.
    """

    @staticmethod
    @abc.abstractmethod
    def from_config(config_path: str):
        """ Creates a client from a config file.

        :param config: The path of the config file to load from
        :type config: str
        :returns: An instance of the created client
        :rtype: AbstractClient
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def start(self) -> None:
        """ Starts the engine.

        :returns: Does not return
        :rtype: None
        """

        raise NotImplementedError()


class BasicClient(AbstractClient):
    """ A very basic client for engine initalization.
    """

    def __init__(self, config: dict):
        """ Initializes the client.

        :param config: A dictionary read in directly from a config file.
        :type config: dict
        """

        device_pairs = []
        pipers = []
        for device in config['devices']:
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
        for piper in config['pipes']:
            piper = getattr(pipe, piper['$'])(**{
                k: v for (k, v) in piper.items() if k != '$'
            })
            pipers.append(piper)
        self.engine = Engine(dict(device_pairs), pipers)

    @staticmethod
    def from_config(config: str):
        """ Creates a BasicClient from a config file.

        :param config: The path of the config file to load from
        :type config: str
        :returns: An instance of the created BasicClient
        :rtype: BasicClient
        """

        config = os.path.abspath(os.path.expanduser(config))
        if os.path.isfile(config):
            with open(config, 'r') as fp:
                try:
                    return BasicClient(yaml.load(fp))
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
        """ Starts the engine.

        :returns: Does not return
        :rtype: None
        """

        try:
            self.engine.start()
            for _ in self.engine.register.keys():
                _.join()
        except KeyboardInterrupt:
            const.log.info(('terminating client `{self}`').format(self=self))
            self.engine.stop()
