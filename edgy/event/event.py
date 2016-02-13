# -*- coding: utf-8 -*-

class Event(object):
    propagation_stopped = False

    def stop_propagation(self):
        self.propagation_stopped = True
