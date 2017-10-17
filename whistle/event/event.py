# -*- coding: utf-8 -*-

from __future__ import absolute_import


class Event(object):
    propagation_stopped = False

    def stop_propagation(self):
        self.propagation_stopped = True
