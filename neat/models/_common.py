#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc


class AbstractModel(object, metaclass=abc.ABCMeta):
    """ The base class for all valid models.
    """

    @abc.abstractmethod
    def validate(self) -> bool:
        """ Self validates the model.

        :returns: True if valid, otherwise False
        :rtype: bool
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """ Builds a serializable representation of the model.

        :returns: A serializable representation of the model
        :rtype: dict
        """

        raise NotImplementedError()
