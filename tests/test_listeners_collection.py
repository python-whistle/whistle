import random
from random import randint
from unittest.mock import Mock

import pytest

from whistle.listeners import ListenersCollection


def test_interface():
    assert set(filter(lambda x: not x.startswith("_"), dir(ListenersCollection))) == {
        "add",
        "get",
        "has",
        "remove",
        "keys",
        "items",
    }


@pytest.mark.parametrize("event_id", ["event", 42, object()])
def test_sort_listeners(event_id):
    coll = ListenersCollection()

    a, b, c, d, unrelated = Mock(), Mock(), Mock(), Mock(), Mock()

    coll.add(event_id, a)
    coll.add(event_id, b)
    coll.add(event_id, c)

    coll.add("unrelated", unrelated)

    assert coll.get(event_id) == (a, b, c)
    assert coll.has(event_id)
    assert coll.has("unrelated")
    assert not coll.has("something else")
    assert coll.keys() == {event_id, "unrelated"}

    coll.add(event_id, d, priority=-1)
    assert coll.get(event_id) == (d, a, b, c)
    assert coll.has(event_id)
    assert coll.has("unrelated")


@pytest.mark.benchmark
def test_add_benchmark(benchmark):
    coll = ListenersCollection()

    @benchmark
    def add():
        coll.add(f"event{randint(1, 10)}", lambda e: None)


@pytest.mark.benchmark
def test_get_benchmark(benchmark):
    coll = ListenersCollection()
    event_ids = set()
    for i in range(1000):
        event_id = "event_randint(1,10)"
        coll.add(event_id, lambda e: None)
        event_ids.add(event_id)
    event_ids = list(event_ids)

    @benchmark
    def get():
        coll.get(random.choice(event_ids))


@pytest.mark.benchmark
def test_e2e_benchmark(benchmark):
    listeners = {f"event_{i}": Mock() for i in range(1000)}
    coll = ListenersCollection()
    i = 0
    event_ids = list(listeners.keys())

    @benchmark
    def add_get():
        nonlocal i
        event_id = random.choice(event_ids)
        coll.add(event_id, lambda e: None)
        if i % 10 == 0:
            coll.get(event_id)
        i += 1
