#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import urllib

from .. import const
from ._common import AbstractRequester

import blinker
import requests


class ObviusRequester(AbstractRequester):
    """ The requester for the Obvius server.
    """

    _request_endpoint = '/setup/devicexml.cgi'

    def __init__(
        self, device_id: int, obvius_ip: str,
        obvius_user: str, obvius_pass: str, obvius_port: int=80,
        timeout: int=10, **kwargs: dict
    ):
        """ The Obvius requester initializer.

        :param device_id: The id of the Obvius device to request
        :type device_id: int
        :param obvius_ip: The IP of the Obvius server
        :type obvius_ip: str
        :param obvius_user: The auth username of the Obvius server
        :type obvius_user: str
        :param obvius_pass: The auth password of the Obvius server (readonly)
        :type obvius_pass: str
        :param obvius_port: The port of the Obvius server (80)
        :type obvius_port: int
        :param timeout: The request timeout period (10 seconds)
        :type timeout: int
        :param kwargs: Any additional attributes for valid record creation
        :type kwargs: dict
        """

        self._device_id = device_id
        self._timeout = timeout
        (self._obvius_ip, self._obvius_port) = (obvius_ip, obvius_port)
        (self._obvius_user, self._obvius_pass) = (obvius_user, obvius_pass)
        self._meta = kwargs

    def __repr__(self):
        """ Generates string representation of the obvius requester.

        :returns: A string representation of the obvius requester
        :rtype: str
        """

        return ((
            '<{self.__class__.__name__} '
            '({self._obvius_ip}:{self._obvius_port}) {self._device_id}>'
        ).format(self=self))

    def request(self) -> None:
        """ Request information from the obvius.

        :returns: Does not return
        :rtype: None
        """

        const.log.debug((
            'requesting device `{self._device_id}` status from '
            '`{self._obvius_ip}` ...'
        ).format(self=self))
        try:
            requests.get(
                urllib.parse.urljoin(
                    (
                        'http://{self._obvius_ip}:{self._obvius_port}'
                    ).format(self=self),
                    self._request_endpoint
                ),
                auth=(self._obvius_user, self._obvius_pass),
                params={'ADDRESS': self._device_id, 'TYPE': 'DATA'},
                hooks=dict(response=self.receive),
                timeout=self._timeout
            )
        except requests.exceptions.ConnectTimeout as exc:
            const.log.error((
                'connection timeout occured after `{self._timeout}` seconds '
                'for device `{self._device_id}` at `{self._obvius_ip}` ...'
            ).format(self=self))

    def receive(self, resp: requests.Response, *args, **kwargs) -> None:
        """ The receiver of information from the requester.

        :param resp: The response of the request
        :type resp: requests.Response
        :param args: Extra arguments of the request
        :type args: list
        :param kwargs: Extra named arguments of the request
        :type kwargs: dict
        :returns: Does not return
        :rtype: None
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
