from typing import Optional, Protocol

from .event import IEvent
from .listener import IListener


class IAbstractEventDispatcher(Protocol):
    def get_listeners(self, event_id: Optional[str] = None, /):
        ...

    def has_listeners(self, event_id: Optional[str] = None, /):
        ...

    def add_listener(self, event_id: str, listener: IListener, /, *, priority: int = 0):
        ...

    def remove_listener(self, event_id: str, listener: IListener, /):
        ...


class IDispatchedEvent(IEvent, Protocol):
    # todo: add typed var for event dispatcher type
    dispatcher: IAbstractEventDispatcher


class IEventDispatcher(IAbstractEventDispatcher, Protocol):
    def dispatch(self, event_id, event=None, /) -> IDispatchedEvent:
        ...


class IAsyncEventDispatcher(IAbstractEventDispatcher, Protocol):
    async def adispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
        ...
