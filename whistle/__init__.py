from whistle._version import __version__
from whistle.dispatcher import AsyncEventDispatcher, EventDispatcher
from whistle.event import Event
from whistle.protocols import IAsyncEventDispatcher, IEvent, IEventDispatcher

__all__ = [
    "AsyncEventDispatcher",
    "Event",
    "EventDispatcher",
    "IAsyncEventDispatcher",
    "IEvent",
    "IEventDispatcher",
    "__version__",
]
