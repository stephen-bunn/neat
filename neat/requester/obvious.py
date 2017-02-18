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
        self._device_id = device_id
        (self._obvious_ip, self._obvious_port) = (obvious_ip, obvious_port)
        (self._obvious_user, self._obvious_pass) = (obvious_user, obvious_pass)

    @property
    def device_id(self):
        return self._device_id

    @property
    def signal_name(self):
        return self._signal_template.format(self=self)

    @property
    def signal(self):
        return blinker.signal(self.signal_name)

    def request(self):
        const.log.debug((
            'requesting content at `{request_url}` ...'
        ).format(request_url=self._request_template.format(self=self)))
        requests.get(
            self._request_template.format(self=self),
            hooks=dict(response=self.receive)
        )

    def receive(self, resp: requests.Response, *args, **kwargs):
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
