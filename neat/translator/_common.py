#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
from typing import Tuple

import blinker


class AbstractTranslator(object, metaclass=abc.ABCMeta):
    """ The base class for all valid translators.
    """

    signal = blinker.Signal()
    supported_requesters = ()

    # @abc.abstractproperty
    # def supported_requesters(self) -> Tuple[str]:
    #     """ A list of supported requester's class names.
    #     """
    #
    #     raise NotImplementedError()

    @abc.abstractmethod
    def validate(self, data: str) -> bool:
        """ Self validates the data of a supported requester.

        :param data: The data from a supported requester
        :type data: str
        :returns: True if data is valid, otherwise False
        :rtype: bool
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def translate(self, data: str, meta: dict={}) -> None:
        """ Translates some given data into a record.

        :param data: The data returned from a supported requester
        :type data: str
        :param meta: Any additional fields given to the requester
        :type meta: dict
        :returns: Does not return
        :rtype: bool
        """

        raise NotImplementedError()
