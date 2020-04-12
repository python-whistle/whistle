from unittest import mock

import pytest

from whistle import Event, EventDispatcher

STRING_EVENT_ID = '42'
OBJECT_EVENT_ID = object()
NUMERIC_EVENT_ID = 42
STRING_PARAMETER = 'str'
INTEGER_PARAMETER = 42
OBJECT_PARAMETER = object()


class CustomEvent(Event):
    pass


def test_event():
    event = Event()
    assert not event.propagation_stopped

    event.stop_propagation()
    assert event.propagation_stopped


@pytest.mark.parametrize('event_id', [STRING_EVENT_ID, OBJECT_EVENT_ID, NUMERIC_EVENT_ID])
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


@pytest.mark.parametrize('EventType', [Event, CustomEvent])
@pytest.mark.parametrize('event_id', [STRING_EVENT_ID, OBJECT_EVENT_ID, NUMERIC_EVENT_ID])
def test_dispatcher_custom_event(EventType, event_id):
    dispatcher = EventDispatcher()
    listener = mock.MagicMock()
    event = EventType()

    dispatcher.add_listener(event_id, listener)
    e = dispatcher.dispatch(event_id, event=event)

    assert listener.call_count == 1
    assert e == event


@pytest.mark.parametrize('event_id', [STRING_EVENT_ID, OBJECT_EVENT_ID, NUMERIC_EVENT_ID])
@pytest.mark.parametrize('param_1', [STRING_PARAMETER, INTEGER_PARAMETER, OBJECT_PARAMETER])
@pytest.mark.parametrize('param_2', [STRING_PARAMETER, INTEGER_PARAMETER, OBJECT_PARAMETER])
def test_dispatcher_with_args(event_id, param_1, param_2):
    dispatcher = EventDispatcher()
    listener = mock.MagicMock()

    dispatcher.add_listener(event_id, listener)
    e = dispatcher.dispatch(event_id, param_1, param_2)

    assert listener.call_count == 1
    assert (listener.call_args) == ((e, param_1, param_2),)


@pytest.mark.parametrize('EventType', [Event, CustomEvent])
@pytest.mark.parametrize('event_id', [STRING_EVENT_ID, OBJECT_EVENT_ID, NUMERIC_EVENT_ID])
@pytest.mark.parametrize('param_1', [STRING_PARAMETER, INTEGER_PARAMETER, OBJECT_PARAMETER])
@pytest.mark.parametrize('param_2', [STRING_PARAMETER, INTEGER_PARAMETER, OBJECT_PARAMETER])
def test_dispatcher_custom_event_with_args(EventType, event_id, param_1, param_2):
    dispatcher = EventDispatcher()
    listener = mock.MagicMock()
    event = EventType()

    dispatcher.add_listener(event_id, listener)
    e = dispatcher.dispatch(event_id, param_1, param_2, event=event)

    assert listener.call_count == 1
    assert (listener.call_args) == ((e, param_1, param_2),)


def test_propagation():
    dispatcher = EventDispatcher()

    for event_id in (
        STRING_EVENT_ID,
        OBJECT_EVENT_ID,
        NUMERIC_EVENT_ID,
    ):
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

        assert dispatcher.get_listeners(event_id) == [listener1, listener2, listener3]

    listeners = dispatcher.get_listeners()
    assert len(listeners) == 3
    for event_id in (
        STRING_EVENT_ID,
        OBJECT_EVENT_ID,
        NUMERIC_EVENT_ID,
    ):
        assert len(listeners[event_id]) == 3


def test_no_listener():
    dispatcher = EventDispatcher()
    for event_id in (
        STRING_EVENT_ID,
        OBJECT_EVENT_ID,
        NUMERIC_EVENT_ID,
    ):
        assert not dispatcher.has_listeners(event_id)

        e = dispatcher.dispatch(event_id)
        assert not e.propagation_stopped


def test_remove_listener():
    dispatcher = EventDispatcher()

    for event_id in (
        STRING_EVENT_ID,
        OBJECT_EVENT_ID,
        NUMERIC_EVENT_ID,
    ):
        listener = mock.MagicMock()
        assert not dispatcher.has_listeners(event_id)

        dispatcher.remove_listener(event_id, listener)
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


def test_listen_decorator():
    dispatcher = EventDispatcher()

    for event_id in (
        STRING_EVENT_ID,
        OBJECT_EVENT_ID,
        NUMERIC_EVENT_ID,
    ):
        listener = mock.MagicMock()
        dispatcher.listen(event_id)(listener)
        e = dispatcher.dispatch(event_id)
        assert listener.call_count == 1
        assert not e.propagation_stopped
