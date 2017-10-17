# -*- coding: utf-8 -*-

from __future__ import absolute_import

import operator

from edgy.event.event import Event


class EventDispatcher(object):
    def __init__(self):
        self._listeners = {}
        self._sorted = {}

    def dispatch(self, event_id, event=None):
        if event is None:
            event = Event()

        event.dispatcher = self
        event.name = event_id

        if not event_id in self._listeners:
            return event

        self.do_dispatch(self.get_listeners(event_id), event)

        return event

    def get_listeners(self, event_id=None):
        if event_id is not None:
            if not event_id in self._sorted:
                self.sort_listeners(event_id)

            return self._sorted[event_id]

        for event_id in self._listeners:
            if not event_id in self._sorted:
                self.sort_listeners(event_id)

        return self._sorted

    def has_listeners(self, event_id=None):
        return bool(len(self.get_listeners(event_id)))

    def add_listener(self, event_id, listener, priority=0):
        if not event_id in self._listeners:
            self._listeners[event_id] = {}
        if not priority in self._listeners[event_id]:
            self._listeners[event_id][priority] = []
        self._listeners[event_id][priority].append(listener)

        if event_id in self._sorted:
            del self._sorted[event_id]

    def listen(self, event_id, priority=0):
        """
        Decorator that add the decorated functions as one of this instance listeners, for the given event name.

        :param event_id:
        :param priority:
        :return:

        """

        def wrapper(listener):
            self.add_listener(event_id, listener, priority)
            return listener

        return wrapper

    def remove_listener(self, event_id, listener):
        """
        Remove a fiven listener from this event dispatcher. For now, if the listener is not registered for this event,
        this method has no effect, but we may raise ValueError in the future if the given listener is not found, you
        should catch it if you're not certain the listener is registered.

        TODO raise ValueError if not found.

        :param event_id:
        :param listener:
        :return:
        """
        if not event_id in self._listeners:
            return

        for priority, listeners in self._listeners[event_id].items():
            if listener in self._listeners[event_id][priority]:
                # pylint: disable=filter-builtin-not-iterating
                self._listeners[event_id][priority] = filter(
                    lambda l: l != listener, self._listeners[event_id][priority]
                )
                if event_id in self._sorted:
                    del self._sorted[event_id]

    def do_dispatch(self, listeners, event):
        for listener in listeners:
            listener(event)
            if event.propagation_stopped: break

    def sort_listeners(self, event_id):
        self._sorted[event_id] = []
        if event_id in self._listeners:
            self._sorted[event_id] = [
                listener
                for listeners in sorted(
                    self._listeners[event_id].items(), key=operator.itemgetter(0)
                ) for listener in listeners[1]
            ]
