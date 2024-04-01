import inspect
from typing import Optional, cast

from whistle.dispatchers.base import AbstractEventDispatcher
from whistle.event import Event
from whistle.typing import IDispatchedEvent, IEvent, IListener


class AsyncEventDispatcher(AbstractEventDispatcher):
    """
    Adapts whiste's EventDispatcher to be async.

    .. versionadded:: 2.0

    """

    def add_listener(self, event_id: str, listener: IListener, /, *, priority: int = 0):
        if not inspect.iscoroutinefunction(listener):
            raise TypeError(f"Listener should be a coroutine function, {type(listener)} given")
        return super().add_listener(event_id, listener, priority=priority)

    def dispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
        raise NotImplementedError("AsyncEventDispatcher does not implement sync dispatch")

    async def adispatch(self, event_id: str, event: Optional[IEvent] = None, /) -> IDispatchedEvent:
        """
        :param event_id:
        :param event:
        :return:
        """
        if event is None:
            event = Event()

        event.name = event_id
        event.dispatcher = self

        await self._adispatch(self.get_listeners(event_id), event)
        return cast(IDispatchedEvent, event)

    async def _adispatch(self, listeners, event):
        for listener in listeners:
            await listener(event)
            if event.propagation_stopped:
                break
