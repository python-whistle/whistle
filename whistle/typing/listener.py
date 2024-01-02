from typing import Any, Callable

from .event import IEvent

IListener = Callable[[IEvent], Any]
