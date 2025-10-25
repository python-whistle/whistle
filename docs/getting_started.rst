Getting Started
===============

This guide walks you through creating your first event dispatcher.

Your First Dispatcher
---------------------

Let's create a simple example that demonstrates the basic workflow: create a dispatcher, register a listener, and dispatch an event.

.. literalinclude:: ../examples/example_01_basic_sync.py
    :language: python
    :lines: 8-

Walking Through the Code
------------------------

1. **Import the dispatcher**::

    from whistle import EventDispatcher

   We import ``EventDispatcher`` for synchronous event handling.

2. **Create a dispatcher instance**::

    dispatcher = EventDispatcher()

   Create an instance that will manage events and listeners.

3. **Define a listener function**::

    def on_spectacle_starts(event):
        print("Please turn down your phones!")

   Listeners are regular Python functions that accept an event parameter.

4. **Register the listener**::

    dispatcher.add_listener("spectacle.starts", on_spectacle_starts)

   Connect the listener to a specific event name.

5. **Dispatch the event**::

    dispatcher.dispatch("spectacle.starts")

   Trigger the event - all registered listeners will be called.

Running the Example
-------------------

Save the code to a file and run it:

.. code-block:: shell

    python example_01_basic_sync.py

Output::

    Please turn down your phones!

Next Steps
----------

Now that you understand the basics:

* Learn about :doc:`synchronous` for more sync patterns
* Explore :doc:`asynchronous` for async/await usage
* Discover :doc:`priorities` to control execution order
* Master :doc:`propagation` to control event flow
