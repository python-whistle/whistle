import inspect
from typing import Optional, cast

from whistle.dispatchers.base import AbstractEventDispatcher
from whistle.event import Event
from whistle.typing import IDispatchedEvent, IEvent, IListener


class EventDispatcher(AbstractEventDispatcher):
    """
    Main class of the library, it is responsible for keeping track of registered listeners, and dispatching events to
    them. All listeners are scoped to the event dispatcher instance, so you can have multiple event dispatchers with
    different sets of listeners.

    """

    def add_listener(self, event_id: str, listener: IListener, /, *, priority: int = 0):
        if inspect.iscoroutinefunction(listener):
            raise TypeError(f"Listener should not be a coroutine function, {type(listener)} given")
        return super().add_listener(event_id, listener, priority=priority)

    def dispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
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

        # todo should name be part of dispatched event ?
        event.name = event_id
        event.dispatcher = self

        self.do_dispatch(self._listeners.get(event_id), event)

        return cast(IDispatchedEvent, event)

    async def adispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
        # allows to use the async interface with a sync dispatcher, although this is not recommended
        # todo add a strict mode that raises an error when trying to use async interface with a sync dispatcher
        return self.dispatch(event_id, event)

    def do_dispatch(self, listeners, event: IEvent, /):
        for listener in listeners:
            listener(event)
            if event.propagation_stopped:
                break
