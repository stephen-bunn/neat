#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
Obvius.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-16-2017 15:57:38
    :modified: 02-16-2017 15:57:38
.. moduleauthor:: Stephen Bunn <r>
"""

import blinker
import requests
import urllib

from .. import const
from ._common import AbstractRequester


class ObviusRequester(AbstractRequester):
    """ The requester for the Obvius server.
    """

    _request_endpoint = '/setup/devicexml.cgi'

    def __init__(
        self, device_id: int, Obvius_ip: str,
        Obvius_user: str, Obvius_pass: str, Obvius_port: int=80,
        timeout: int=10, **kwargs: dict
    ):
        """ The Obvius requester initializer.

        :param device_id: The id of the Obvius device to request
        :type device_id: int
        :param Obvius_ip: The IP of the Obvius server
        :type Obvius_ip: str
        :param Obvius_user: The auth username of the Obvius server
        :type Obvius_user: str
        :param Obvius_pass: The auth password of the Obvius server (readonly)
        :type Obvius_pass: str
        :param Obvius_port: The port of the Obvius server (80)
        :type Obvius_port: int
        :param timeout: The request timeout period (10 seconds)
        :type timeout: int
        """

        self._device_id = device_id
        self._timeout = timeout
        (self._Obvius_ip, self._Obvius_port) = (Obvius_ip, Obvius_port)
        (self._Obvius_user, self._Obvius_pass) = (Obvius_user, Obvius_pass)
        self._meta = kwargs

    def __repr__(self):
        """ Generates string representation of the Obvius requester.

        :returns: A string representation of the Obvius requester
        :rtype: str
        """

        return ((
            '<{self.__class__.__name__} '
            '({self._Obvius_ip}:{self._Obvius_port}) {self._device_id}>'
        ).format(self=self))

    def request(self) -> None:
        """ Request information from the Obvius.
        """

        const.log.debug((
            'requesting device `{self._device_id}` status from '
            '`{self._Obvius_ip}` ...'
        ).format(self=self))
        try:
            requests.get(
                urllib.parse.urljoin(
                    (
                        'http://{self._Obvius_ip}:{self._Obvius_port}'
                    ).format(self=self),
                    self._request_endpoint
                ),
                auth=(self._Obvius_user, self._Obvius_pass),
                params={'ADDRESS': self._device_id, 'TYPE': 'DATA'},
                hooks=dict(response=self.receive),
                timeout=self._timeout
            )
        except requests.exceptions.ConnectTimeout as exc:
            const.log.error((
                'connection timeout occured after `{self._timeout}` seconds '
                'for device `{self._device_id}` at `{self._Obvius_ip}` ...'
            ).format(self=self))

    def receive(self, resp: requests.Response, *args, **kwargs) -> None:
        """ The receiver of information from the requester.

        :param resp: The response of the request
        :type resp: requests.Response
        :param args: Extra arguments of the request
        :type args: list
        :param kwargs: Extra named arguments of the request
        :type kwargs: dict
        """

        if resp.status_code == 200:
            const.log.debug((
                'received response from `{resp.url}` ...'
            ).format(resp=resp))
            self.signal.send(self, data=resp.text, meta=self._meta)
        else:
            const.log.error((
                'received invalid response from `{resp.url}` '
                '({resp.status_code}) ...'
            ).format(resp=resp))
