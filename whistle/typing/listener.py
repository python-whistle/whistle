from typing import Any, Callable, Coroutine, Union

from .event import IEvent

# todo: async vs sync listeners to help IDEs more ?
IListener = Callable[[IEvent], Union[Any, Coroutine]]
