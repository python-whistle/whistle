# -*- coding: utf-8 -*-

from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    import mock

from edgy.event import Event, EventDispatcher

STRING_EVENT_ID = '42'
OBJECT_EVENT_ID = object()
NUMERIC_EVENT_ID = 42


class BasicTest(TestCase):
    def test_event(self):
        event = Event()
        assert not event.propagation_stopped

        event.stop_propagation()
        assert event.propagation_stopped

    def test_dispatcher(self):
        dispatcher = EventDispatcher()

        for event_id in (
            STRING_EVENT_ID,
            OBJECT_EVENT_ID,
            NUMERIC_EVENT_ID,
        ):
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

    def test_propagation(self):
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

            self.assertSequenceEqual(dispatcher.get_listeners(event_id), (listener1, listener2, listener3))

        listeners = dispatcher.get_listeners()
        assert len(listeners) == 3
        for event_id in (
            STRING_EVENT_ID,
            OBJECT_EVENT_ID,
            NUMERIC_EVENT_ID,
        ):
            assert len(listeners[event_id]) == 3

    def test_no_listener(self):
        dispatcher = EventDispatcher()
        for event_id in (
            STRING_EVENT_ID,
            OBJECT_EVENT_ID,
            NUMERIC_EVENT_ID,
        ):
            assert not dispatcher.has_listeners(event_id)

            e = dispatcher.dispatch(event_id)
            assert not e.propagation_stopped

    def test_remove_listener(self):
        dispatcher = EventDispatcher()

        for event_id in (
            STRING_EVENT_ID,
            OBJECT_EVENT_ID,
            NUMERIC_EVENT_ID,
        ):
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

    def test_listen_decorator(self):
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
