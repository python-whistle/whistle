Synchronous Dispatching
=======================

The ``EventDispatcher`` class provides synchronous, blocking event dispatching. Use this when your listeners perform regular (non-async) operations.

When to Use EventDispatcher
----------------------------

Choose ``EventDispatcher`` when:

* Your listeners perform synchronous operations (database queries, file I/O, calculations)
* You're working with existing synchronous code
* You don't need async/await functionality
* You want simpler, more straightforward code flow

Creating a Dispatcher
---------------------

Create an instance of ``EventDispatcher``::

    from whistle import EventDispatcher

    dispatcher = EventDispatcher()

All listeners registered with this dispatcher must be regular (synchronous) functions. Attempting to register an async function will raise a ``TypeError``.

Multiple Listeners
------------------

Multiple listeners can respond to the same event. They execute in the order they were registered (when no priority is specified):

.. literalinclude:: ../examples/example_02_sync_multiple_listeners.py
    :language: python
    :lines: 8-

Running this example produces::

    1. Turning off the lights
    2. Starting the music
    3. Opening the curtains

All three listeners execute sequentially when the event is dispatched.

Using the @listen Decorator
----------------------------

For cleaner code, use the ``@listen`` decorator to register listeners:

.. literalinclude:: ../examples/example_03_sync_decorator.py
    :language: python
    :lines: 8-

The decorator provides a more elegant syntax and makes the event-listener relationship clear at the point of definition.

Dispatching Events
------------------

The ``dispatch()`` method triggers an event::

    event = dispatcher.dispatch("event.name")

Key behaviors:

* If no ``Event`` object is provided, the dispatcher creates one automatically
* The event object is passed to all registered listeners
* Listeners execute sequentially in priority order
* The event object is returned after all listeners execute

Providing Custom Events
-----------------------

You can provide your own event object::

    from whistle import Event

    custom_event = Event()
    custom_event.my_data = "some value"

    dispatcher.dispatch("event.name", custom_event)

Listeners can then access ``event.my_data``. See :doc:`custom_events` for more details on creating custom event classes.

API Summary
-----------

``EventDispatcher`` provides:

* ``add_listener(event_id, listener, priority=0)``: Register a listener
* ``remove_listener(event_id, listener)``: Unregister a listener
* ``listen(event_id, priority=0)``: Decorator for registering listeners
* ``dispatch(event_id, event=None)``: Trigger an event synchronously
* ``get_listeners(event_id=None)``: Retrieve registered listeners
* ``has_listeners(event_id=None)``: Check if listeners are registered

See also :doc:`asynchronous` for the async equivalent.
