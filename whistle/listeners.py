from collections import defaultdict

from whistle.errors import RemovedInWhistle2Error
from whistle.typing import IListener


class ListenersCollection:
    def __init__(self) -> None:
        self._items = defaultdict(lambda: defaultdict(list))
        self._sorted = {}

    def add(self, event_id: str, listener: IListener, /, *, priority: int = 0) -> None:
        """
        Add a listener for the given event id, with the given priority.

        Priority must be a number between -127 and 128, inclusive. As a convention coming from unix process priorities,
        we use priorities ranging from -20 (highest priority) to 20 (lowest priority), with 0 being the default
        priority.

        The actual permited range is so because python dicts are WAY faster with string keys than integers. This fact
        still puzzles me but the difference is huge. The same rationale applies to the event_id parameter: although we
        could support arbitrary hashable values as event ids (and we encouraged so in whistle 1.x), we now restrict it
        to strings for performance reasons.

        :param event_id: string identifier for the event
        :param listener: callback to be called when the event is dispatched
        :param priority: integer priority for the listener (-20 (high) to 19 (low))

        """

        if not callable(listener):
            raise TypeError(f"Listener should be a callable, {type(listener)} given")

        # priority = chr(priority)
        self._items[event_id][priority].append(listener)
        if event_id in self._sorted:
            del self._sorted[event_id]

    def get(self, event_id: str, /) -> tuple[IListener, ...]:
        """
        Gets the listeners for the given event id, in order of priority.

        :param event_id: string identifier for the event

        """
        if event_id is None:
            raise RemovedInWhistle2Error("ListenersCollection.get() without event_id is not accepted anymore.")

        if event_id not in self._items:
            return ()

        if event_id not in self._sorted:
            self._sort(event_id)

        return self._sorted[event_id]

    def has(self, event_id: str, /) -> bool:
        # todo avoid sort for has !!!
        return bool(len(self.get(event_id)))

    def remove(self, event_id: str, listener: IListener, /) -> None:
        """ """
        if event_id not in self._items:
            raise ValueError(f"Listener {listener} is not registered for event {event_id}.")

        for priority, listeners in self._items[event_id].items():
            if listener in listeners:
                self._items[event_id][priority] = list(filter(lambda _listener: _listener != listener, listeners))

        if event_id in self._sorted:
            del self._sorted[event_id]

    def keys(self):
        return self._items.keys()

    def items(self):
        for event_id in self.keys():
            yield event_id, self.get(event_id)

    def _sort(self, event_id, /):
        # set to an empty list just in case some concurrent access happens
        _sorted = ()
        self._sorted[event_id] = _sorted

        for priority in sorted(self._items.get(event_id, {}).keys()):
            _sorted += tuple(self._items[event_id][priority])

        self._sorted[event_id] = _sorted
