from typing import Protocol


class IEvent(Protocol):
    name: str
    propagation_stopped: bool

    def stop_propagation(self):
        ...
