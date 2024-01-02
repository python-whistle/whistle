from typing import Any, Callable, Coroutine

from .event import IEvent

# todo: async vs sync listeners to help IDEs more ?
IListener = Callable[[IEvent], Any | Coroutine]
