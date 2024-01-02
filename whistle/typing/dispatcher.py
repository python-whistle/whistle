from typing import Protocol

from .event import IEvent


class IAbstractEventDispatcher(Protocol):
    ...


class IDispatchedEvent(IEvent, Protocol):
    # todo: add typed var for event dispatcher type
    dispatcher: IAbstractEventDispatcher


class IEventDispatcher(IAbstractEventDispatcher, Protocol):
    def dispatch(self, event_id, event=None, /) -> IDispatchedEvent:
        ...


class IAsyncEventDispatcher(IAbstractEventDispatcher, Protocol):
    async def dispatch(self, event_id, event=None, /) -> IDispatchedEvent:
        ...
