from functools import cached_property

from whistle.event import Event
from whistle.listeners import ListenersCollection


class EventDispatcher(object):
    """
    Main class of the library, it is responsible for keeping track of registered listeners, and dispatching events to
    them. All listeners are scoped to the event dispatcher instance, so you can have multiple event dispatchers with
    different sets of listeners.

    """

    def __init__(self):
        self._listeners = ListenersCollection()
        self._old_listeners = {}
        self._sorted = {}

    @cached_property
    def listeners(self):
        # todo test we cannot change reference
        return self._listeners

    def dispatch(self, event_id, event=None, /):
        """
        Dispatch the given event, with the given event id.

        An optional event can be given, and should respect the :class:`whistle.protocols.IEvent` protocol.
        If no event is given, a new :class:`whistle.event.Event` instance is created and used.

        Returns the event instance after it has been dispatched, whether it has been created or provided by the caller.

        :param event_id: hashable identifier for the event
        :param event: optional event instance
        :return: the event instance after it has been dispatched

        """
        if event is None:
            event = Event()

        event.dispatcher = self
        event.name = event_id

        self.do_dispatch(self._listeners.get(event_id), event)

        return event

    def listen(self, event_id, priority=0):
        """
        Decorator that add the decorated functions as one of this instance listeners, for the given event name.

        :param event_id:
        :param priority:
        :return:

        """

        def wrapper(listener):
            self._listeners.add(event_id, listener, priority=priority)
            return listener

        return wrapper

    def do_dispatch(self, listeners, event):
        for listener in listeners:
            listener(event)
            if event.propagation_stopped:
                break

    def get_listeners(self, event_id=None):
        # deprecated compatibility method
        return self._listeners.get(event_id)

    def has_listeners(self, event_id=None):
        # deprecated compatibility method
        return self._listeners.has(event_id)

    def add_listener(self, event_id, listener, priority=0):
        # deprecated compatibility method
        return self._listeners.add(event_id, listener, priority=priority)

    def remove_listener(self, event_id, listener):
        # deprecated compatibility method
        return self._listeners.remove(event_id, listener)


class AsyncEventDispatcher(EventDispatcher):
    """
    Adapts whiste's EventDispatcher to be async. Probably should go into whistle 2.x?
    """

    async def do_dispatch(self, listeners, event):
        for listener in listeners:
            await listener(event)
            if event.propagation_stopped:
                break

    async def dispatch(self, event_id, event=None):
        """
        todo: add this as dispatch_async in whistle 2.0 ?

        :param event_id:
        :param event:
        :return:
        """
        if event is None:
            event = Event()

        event.dispatcher = self
        event.name = event_id

        if event_id not in self._listeners:
            return event

        await self.do_dispatch(self.get_listeners(event_id), event)

        return event
