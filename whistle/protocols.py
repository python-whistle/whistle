from typing import Protocol

from whistle.listeners import ListenersCollection


class IBaseEventDispatcher(Protocol):
    listeners: ListenersCollection


class IEvent(Protocol):
    name: str
    dispatcher: IBaseEventDispatcher
    propagation_stopped: bool

    def stop_propagation(self):
        ...


class IEventDispatcher(IBaseEventDispatcher, Protocol):
    def dispatch(self, event_id, event=None, /) -> IEvent:
        ...


class IAsyncEventDispatcher(IBaseEventDispatcher, Protocol):
    async def dispatch(self, event_id, event=None, /) -> IEvent:
        ...
