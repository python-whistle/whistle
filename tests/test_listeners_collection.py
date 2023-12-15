from whistle.listeners import ListenersCollection


def test_sort_listeners():
    coll = ListenersCollection()

    coll.add("event", "a")
    coll.add("event", "b")
    coll.add("event", "c")

    coll._sort("event")
    assert coll._sorted == {"event": ("a", "b", "c")}

    coll.add("event", "d", priority=-1)
    assert coll._sorted == {}

    coll._sort("event")
    assert coll._sorted == {"event": ("d", "a", "b", "c")}
