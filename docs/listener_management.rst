Listener Management
===================

Beyond adding listeners, Whistle provides tools to check for listeners, retrieve them, and remove them dynamically.

Checking for Listeners
----------------------

Use ``has_listeners()`` to check if an event has registered listeners::

    if dispatcher.has_listeners("user.login"):
        # Dispatch only if someone is listening
        dispatcher.dispatch("user.login")

This is useful for:

* **Performance optimization**: Skip expensive event object creation
* **Conditional dispatch**: Only dispatch when listeners are present
* **Feature detection**: Check if a plugin or extension is active

Checking Any Listeners
~~~~~~~~~~~~~~~~~~~~~~

Call ``has_listeners()`` without arguments to check if any events have listeners::

    if dispatcher.has_listeners():
        print("Dispatcher has listeners registered")
    else:
        print("No listeners registered")

This is mainly useful for debugging and testing.

Retrieving Listeners
--------------------

Use ``get_listeners()`` to retrieve all listeners for an event::

    listeners = dispatcher.get_listeners("app.start")
    print(f"Number of listeners: {len(listeners)}")

The method returns a tuple of listeners in priority order.

Retrieving All Listeners
~~~~~~~~~~~~~~~~~~~~~~~~~

Call ``get_listeners()`` without arguments to get a dictionary of all events and their listeners::

    all_listeners = dispatcher.get_listeners()

    for event_id, listeners in all_listeners.items():
        print(f"{event_id}: {len(listeners)} listeners")

This is useful for:

* Debugging dispatcher state
* Generating reports
* Testing listener registration

Removing Listeners
------------------

Use ``remove_listener()`` to unregister a specific listener::

    def my_listener(event):
        ...

    # Add it
    dispatcher.add_listener("event", my_listener)

    # Remove it
    dispatcher.remove_listener("event", my_listener)

After removal, the listener will no longer be called when the event is dispatched.

Complete Example
----------------

Here's a full example demonstrating listener management:

.. literalinclude:: ../examples/example_09_listener_management.py
    :language: python
    :lines: 8-

Running this produces::

    === Initial State ===
    Has listeners for 'app.start': False

    === After Registration ===
    Has listeners for 'app.start': True
    Number of listeners: 2

    === Dispatching Event ===
    Listener one executed
    Listener two executed

    === After Removing listener_two ===
    Number of listeners: 1

    === Dispatching Event Again ===
    Listener one executed

    === Global Check ===
    Dispatcher has any listeners: True

Use Cases
---------

Dynamic Plugin Management
~~~~~~~~~~~~~~~~~~~~~~~~~

Load and unload plugins at runtime::

    class Plugin:
        def __init__(self, dispatcher):
            self.dispatcher = dispatcher
            self.listeners = []

        def register(self):
            listener = lambda event: self.on_event(event)
            self.dispatcher.add_listener("app.event", listener)
            self.listeners.append(("app.event", listener))

        def unregister(self):
            for event_id, listener in self.listeners:
                self.dispatcher.remove_listener(event_id, listener)
            self.listeners.clear()

    # Install plugin
    plugin = Plugin(dispatcher)
    plugin.register()

    # Uninstall plugin
    plugin.unregister()

Conditional Dispatch
~~~~~~~~~~~~~~~~~~~~

Optimize by checking before expensive operations::

    def publish_metrics(metrics_data):
        # Skip expensive serialization if no one is listening
        if not dispatcher.has_listeners("metrics.publish"):
            return

        # Only create event if listeners exist
        event = MetricsEvent(metrics_data)
        dispatcher.dispatch("metrics.publish", event)

Testing and Debugging
~~~~~~~~~~~~~~~~~~~~~

Verify listener registration in tests::

    def test_plugin_registers_listeners():
        plugin = MyPlugin(dispatcher)
        plugin.install()

        # Verify listeners were registered
        assert dispatcher.has_listeners("plugin.event")

        listeners = dispatcher.get_listeners("plugin.event")
        assert len(listeners) == 2

    def test_plugin_cleanup():
        plugin = MyPlugin(dispatcher)
        plugin.install()
        plugin.uninstall()

        # Verify listeners were removed
        assert not dispatcher.has_listeners("plugin.event")

Temporary Listeners
~~~~~~~~~~~~~~~~~~~

Add listeners for specific operations then remove them::

    def temporary_operation():
        # Add temporary logging
        def temp_logger(event):
            log.debug(f"Temporary log: {event.name}")

        dispatcher.add_listener("operation.step", temp_logger)

        try:
            # Perform operation
            perform_steps()
        finally:
            # Clean up
            dispatcher.remove_listener("operation.step", temp_logger)

Important Notes
---------------

Reference Equality
~~~~~~~~~~~~~~~~~~

``remove_listener()`` uses reference equality. This won't work::

    # Add with lambda
    dispatcher.add_listener("event", lambda e: print(e))

    # Can't remove - different lambda object
    dispatcher.remove_listener("event", lambda e: print(e))  # Error!

Store a reference to remove later::

    listener = lambda e: print(e)
    dispatcher.add_listener("event", listener)
    dispatcher.remove_listener("event", listener)  # Works

Removing During Dispatch
~~~~~~~~~~~~~~~~~~~~~~~~~

You can safely remove listeners during event dispatch, but they won't affect the current dispatch cycle::

    def self_removing_listener(event):
        print("Executing once")
        event.dispatcher.remove_listener("event", self_removing_listener)

    dispatcher.add_listener("event", self_removing_listener)

    dispatcher.dispatch("event")  # Prints "Executing once"
    dispatcher.dispatch("event")  # Nothing happens (listener removed)

API Reference
-------------

``has_listeners(event_id=None)``
    Check if listeners are registered. Without ``event_id``, checks if any listeners exist.

``get_listeners(event_id=None)``
    Get listeners for an event as a tuple. Without ``event_id``, returns dict of all events.

``remove_listener(event_id, listener)``
    Remove a specific listener. Raises ``ValueError`` if listener not found.

See also :doc:`patterns` for practical examples of listener management.
