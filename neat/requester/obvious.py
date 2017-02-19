#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
obvious.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-16-2017 15:57:38
    :modified: 02-16-2017 15:57:38
.. moduleauthor:: Stephen Bunn <r>
"""

import blinker
import requests

from .. import const
from ._common import AbstractRequester


class ObviousRequester(AbstractRequester):
    """ The requester for the Obvious server.
    """

    _signal_template = (
        '{self.__class__.__name__}_{self._obvious_ip}:{self._obvious_port}_'
        '{self._device_id}'
    )
    _request_template = (
        'http://{self._obvious_user}:{self._obvious_pass}'
        '@{self._obvious_ip}:{self._obvious_port}'
        '/setup/devicexml.cgi?ADDRESS={self._device_id}&TYPE=DATA'
    )

    def __init__(
        self, device_id: int, obvious_ip: str,
        obvious_user: str, obvious_pass: str, obvious_port: int=80
    ):
        """ The Obvious requester initializer.

        :param device_id: The id of the Obvious device to request
        :type device_id: int
        :param obvious_ip: The IP of the Obvious server
        :type obvious_ip: str
        :param obvious_user: The auth username of the Obvious server
        :type obvious_user: str
        :param obvious_pass: The auth password of the Obvious server (readonly)
        :type obvious_pass: str
        :param obvious_port: The port of the Obvious server (80)
        :type obvious_port: int
        """

        self._device_id = device_id
        (self._obvious_ip, self._obvious_port) = (obvious_ip, obvious_port)
        (self._obvious_user, self._obvious_pass) = (obvious_user, obvious_pass)

    @property
    def device_id(self) -> int:
        """ The id of the Obvious device for the requester.
        """

        return self._device_id

    @property
    def signal_name(self) -> str:
        """ The signal name of the Obvious requester.
        """

        return self._signal_template.format(self=self)

    @property
    def signal(self) -> blinker.Signal:
        """ The signal of the Obvious requester.
        """

        return blinker.signal(self.signal_name)

    def request(self) -> None:
        """ Request information from the Obvious.
        """

        const.log.debug((
            'requesting content at `{request_url}` ...'
        ).format(request_url=self._request_template.format(self=self)))
        requests.get(
            self._request_template.format(self=self),
            hooks=dict(response=self.receive)
        )

    def receive(self, resp: requests.Response, *args, **kwargs) -> None:
        """ The reciever of information from the requester.

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
            self.signal.send(self, data=resp.text)
        else:
            const.log.error((
                'received invalid response from `{resp.url}` '
                '({resp.status_code}) ...'
            ).format(resp=resp))
