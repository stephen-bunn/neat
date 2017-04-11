#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
from typing import Tuple

import blinker


class AbstractTranslator(object, metaclass=abc.ABCMeta):
    signal = blinker.Signal()

    @abc.abstractproperty
    def supported_requesters(self) -> Tuple[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self, content: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def translate(self, content: str) -> dict:
        raise NotImplementedError()
