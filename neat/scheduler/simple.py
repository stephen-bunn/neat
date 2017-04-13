#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import time

from .. import const
from ._common import AbstractScheduler


class SimpleDelayScheduler(AbstractScheduler):
    """ The scheduler for simple requesters.

    .. note:: Required, that all subclasses call super initialization
    """

    def __init__(self, delay: float=1.0):
        """ The SimpleDelayScheduler scheduler initializer.

        :param delay: The delay to wait in between requests
        :type delay: float
        """

        super().__init__()
        self.delay = delay

    def __repr__(self):
        """ A string representation of the scheduler object.

        :returns: A string representation of the scheduler object
        :rtype: str
        """

        return (
            '<{self.name} delay={self.delay}>'
        ).format(self=self)

    @property
    def delay(self) -> float:
        """ The delay period in between scheduled requests.
        """

        return self._delay

    @delay.setter
    def delay(self, delay: float) -> None:
        """ Sets the scheduler's delay.

        :param delay: The new delay of the scheduler
        :type delay: float
        """
        self._delay = float(delay)

    def run(self) -> None:
        """ Starts the infinite loop for signaling scheduled requests.

        :returns: Does not return
        :rtype: None
        """

        self.daemon = True
        while self.is_alive():
            self.signal.send(self)
            try:
                time.sleep(self.delay)
            except KeyboardInterrupt as exc:
                const.log.debug((
                    'scheduler `{self}` was terminated ...'
                ).format(self=self))
                break
