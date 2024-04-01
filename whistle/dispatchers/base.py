from abc import ABCMeta, abstractmethod
from typing import Optional

from whistle.listeners import ListenersCollection
from whistle.typing import IDispatchedEvent, IEvent, IListener


class AbstractEventDispatcher(metaclass=ABCMeta):
    def __init__(self):
        self._listeners = ListenersCollection()

    def get_listeners(self, event_id: Optional[str] = None, /):
        # compatibility with 1.x
        if event_id is None:
            return {event_id: self._listeners.get(event_id) for event_id in self._listeners.keys()}

        return self._listeners.get(event_id)

    def has_listeners(self, event_id: Optional[str] = None, /):
        # compatibility with 1.x
        if event_id is None:
            return bool(len(self._listeners.keys()))

        return self._listeners.has(event_id)

    def add_listener(self, event_id: str, listener: IListener, /, *, priority: int = 0):
        return self._listeners.add(event_id, listener, priority=priority)

    def remove_listener(self, event_id: str, listener: IListener, /):
        # deprecated compatibility method
        return self._listeners.remove(event_id, listener)

    def listen(self, event_id: str, /, *, priority=0):
        """
        Decorator that add the decorated functions as one of this instance listeners, for the given event name.

        deperecated ?

        :param event_id:
        :param priority:
        :return:

        """

        def wrapper(listener):
            self._listeners.add(event_id, listener, priority=priority)
            return listener

        return wrapper

    @abstractmethod
    def dispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
        ...

    @abstractmethod
    async def adispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
        ...
