import operator


class ListenersCollection:
    def __init__(self):
        self._items = {}
        self._sorted = {}

    def add(self, event_id, listener, /, *, priority=0):
        if event_id not in self._items:
            self._items[event_id] = {}
        if priority not in self._items[event_id]:
            self._items[event_id][priority] = []
        self._items[event_id][priority].append(listener)

        if event_id in self._sorted:
            del self._sorted[event_id]

    def get(self, event_id, /):
        if event_id is not None:
            if event_id not in self._sorted:
                self._sort(event_id)
            return self._sorted[event_id]

        for event_id in self._items:
            if event_id not in self._sorted:
                self._sort(event_id)

        return self._sorted

    __getitem__ = get

    def has(self, event_id, /):
        return bool(len(self.get(event_id)))

    __contains__ = has

    def remove(self, event_id, listener, /):
        """ """
        if event_id not in self._items:
            raise ValueError(f"Listener {listener} is not registered for event {event_id}.")

        for priority, listeners in self._items[event_id].items():
            if listener in listeners:
                # pylint: disable=filter-builtin-not-iterating
                self._items[event_id][priority] = list(filter(lambda _listener: _listener != listener, listeners))

        if event_id in self._sorted:
            del self._sorted[event_id]

    def _sort(self, event_id, /):
        self._sorted[event_id] = []
        if event_id in self._items:
            self._sorted[event_id] = tuple(
                listener
                for listeners in sorted(self._items[event_id].items(), key=operator.itemgetter(0))
                for listener in listeners[1]
            )
