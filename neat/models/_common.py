#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc


class AbstractModel(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()
