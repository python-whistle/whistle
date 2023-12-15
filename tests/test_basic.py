from unittest import mock

import pytest

from whistle import Event, EventDispatcher

STRING_EVENT_ID = "42"
OBJECT_EVENT_ID = object()
NUMERIC_EVENT_ID = 42

BUNCH_OF_EVENT_IDS = [STRING_EVENT_ID, OBJECT_EVENT_ID, NUMERIC_EVENT_ID]


class CustomEvent(Event):
    pass


def parametrize_with_event_id():
    return pytest.mark.parametrize("event_id", BUNCH_OF_EVENT_IDS)


def test_event():
    event = Event()
    assert not event.propagation_stopped

    event.stop_propagation()
    assert event.propagation_stopped


@parametrize_with_event_id()
def test_dispatcher(event_id):
    dispatcher = EventDispatcher()

    listener = mock.MagicMock()
    assert not dispatcher.has_listeners(event_id)
    dispatcher.add_listener(event_id, listener)
    assert dispatcher.has_listeners(event_id)

    assert listener.call_count == 0

    e = dispatcher.dispatch(event_id)

    assert listener.call_count == 1
    assert not e.propagation_stopped

    e = dispatcher.dispatch(event_id)

    assert listener.call_count == 2
    assert not e.propagation_stopped


@pytest.mark.parametrize("EventType", [Event, CustomEvent])
@parametrize_with_event_id()
def test_dispatcher_custom_event(EventType, event_id):
    dispatcher = EventDispatcher()
    listener = mock.MagicMock()
    event = EventType()

    dispatcher.add_listener(event_id, listener)
    e = dispatcher.dispatch(event_id, event)

    assert listener.call_count == 1
    assert e == event


def test_propagation():
    dispatcher = EventDispatcher()

    for event_id in BUNCH_OF_EVENT_IDS:
        listener1 = mock.MagicMock()

        def listener2(event):
            event.stop_propagation()

        listener3 = mock.MagicMock()

        dispatcher.add_listener(event_id, listener1)
        dispatcher.add_listener(event_id, listener2)
        dispatcher.add_listener(event_id, listener3)

        assert listener1.call_count == 0
        assert listener3.call_count == 0

        e = dispatcher.dispatch(event_id)

        assert listener1.call_count == 1
        assert listener3.call_count == 0
        assert e.propagation_stopped

        e = dispatcher.dispatch(event_id)

        assert listener1.call_count == 2
        assert listener3.call_count == 0
        assert e.propagation_stopped

        assert dispatcher.get_listeners(event_id) == (listener1, listener2, listener3)

    listeners = dispatcher.get_listeners()
    assert len(listeners) == 3
    for event_id in BUNCH_OF_EVENT_IDS:
        assert len(listeners[event_id]) == 3


def test_no_listener():
    dispatcher = EventDispatcher()
    for event_id in BUNCH_OF_EVENT_IDS:
        assert not dispatcher.has_listeners(event_id)

        e = dispatcher.dispatch(event_id)
        assert not e.propagation_stopped


def test_remove_listener():
    dispatcher = EventDispatcher()

    for event_id in BUNCH_OF_EVENT_IDS:
        listener = mock.MagicMock()
        assert not dispatcher.has_listeners(event_id)
        dispatcher.add_listener(event_id, listener)
        assert dispatcher.has_listeners(event_id)

        assert listener.call_count == 0

        e = dispatcher.dispatch(event_id)

        assert listener.call_count == 1
        assert not e.propagation_stopped

        assert dispatcher.has_listeners(event_id)
        dispatcher.remove_listener(event_id, listener)
        assert not dispatcher.has_listeners(event_id)

        e = dispatcher.dispatch(event_id)

        assert listener.call_count == 1
        assert not e.propagation_stopped


@parametrize_with_event_id()
def test_listen_decorator(event_id):
    dispatcher = EventDispatcher()
    listener = mock.MagicMock()

    dispatcher.listen(event_id)(listener)
    e = dispatcher.dispatch(event_id)

    assert listener.call_count == 1
    assert not e.propagation_stopped


@parametrize_with_event_id()
def test_first_event_will_get_reference_to_dispatcher_and_name(event_id):
    dispatcher = EventDispatcher()
    listener = mock.MagicMock()

    dispatcher.add_listener(event_id, listener)
    e = dispatcher.dispatch(event_id)

    assert listener.call_count == 1
    assert not e.propagation_stopped
    assert e.dispatcher == dispatcher
    assert e.name == event_id
