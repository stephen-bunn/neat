#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc

import blinker


class AbstractRequester(object, metaclass=abc.ABCMeta):
    """ The abstract class for requester classes.
    """

    signal = blinker.Signal()

    @abc.abstractmethod
    def request(self) -> None:
        """ The requester method for making requests.

        :returns: Does not return
        :rtype: None
        """

        raise NotImplementedError()
