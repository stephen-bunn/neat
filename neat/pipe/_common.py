#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
from typing import List

from ..models import Record

import blinker


class AbstractPipe(object, metaclass=abc.ABCMeta):
    signal = blinker.Signal()

    @abc.abstractmethod
    def accept(self, record: Record) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError()
