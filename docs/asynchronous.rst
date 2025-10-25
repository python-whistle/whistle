Asynchronous Dispatching
========================

The ``AsyncEventDispatcher`` class provides asynchronous event dispatching using async/await. Use this when your listeners perform async operations.

When to Use AsyncEventDispatcher
---------------------------------

Choose ``AsyncEventDispatcher`` when:

* Your listeners perform async I/O operations (database queries, HTTP requests, file operations)
* You're working in an async/await application
* You want non-blocking event handling
* You need to coordinate multiple async operations

Creating an Async Dispatcher
-----------------------------

Create an instance of ``AsyncEventDispatcher``::

    from whistle import AsyncEventDispatcher

    dispatcher = AsyncEventDispatcher()

All listeners registered with this dispatcher must be async functions (coroutines). Attempting to register a regular function will raise a ``TypeError``.

Basic Async Dispatching
------------------------

Here's a simple async example:

.. literalinclude:: ../examples/example_04_basic_async.py
    :language: python
    :lines: 8-

Key differences from synchronous dispatching:

* Listeners are defined with ``async def``
* Listeners can use ``await`` for async operations
* Events are dispatched with ``await dispatcher.adispatch()``
* The entire workflow must run in an async context (``asyncio.run()``)

Async I/O Operations
---------------------

The real power of ``AsyncEventDispatcher`` comes from coordinating async I/O:

.. literalinclude:: ../examples/example_05_async_io_operations.py
    :language: python
    :lines: 8-

This example simulates database writes and API calls. Each listener can perform async operations, but they execute **sequentially** (one after another, not concurrently).

Key Differences from EventDispatcher
-------------------------------------

Type Safety
~~~~~~~~~~~

``AsyncEventDispatcher`` enforces async listeners::

    dispatcher = AsyncEventDispatcher()

    # This works - async function
    async def async_listener(event):
        await some_async_operation()

    dispatcher.add_listener("event", async_listener)  # ✓

    # This raises TypeError - sync function not allowed
    def sync_listener(event):
        some_sync_operation()

    dispatcher.add_listener("event", sync_listener)  # ✗ TypeError

Dispatch Method
~~~~~~~~~~~~~~~

``AsyncEventDispatcher`` only supports async dispatching:

* ``adispatch(event_id, event=None)``: Async dispatch (use this)
* ``dispatch(event_id, event=None)``: Raises ``NotImplementedError``

You must use ``await dispatcher.adispatch()`` - the synchronous ``dispatch()`` method is not implemented.

Sequential Execution
~~~~~~~~~~~~~~~~~~~~

Important: Listeners execute **sequentially**, not concurrently. Each listener completes before the next begins::

    @dispatcher.listen("event")
    async def first(event):
        await asyncio.sleep(1)  # Takes 1 second
        print("First done")

    @dispatcher.listen("event")
    async def second(event):
        await asyncio.sleep(1)  # Takes 1 second
        print("Second done")

    await dispatcher.adispatch("event")  # Takes 2 seconds total

If you need concurrent execution, dispatch multiple events concurrently or use ``asyncio.gather()`` within a listener.

API Summary
-----------

``AsyncEventDispatcher`` provides:

* ``add_listener(event_id, listener, priority=0)``: Register an async listener
* ``remove_listener(event_id, listener)``: Unregister a listener
* ``listen(event_id, priority=0)``: Decorator for registering listeners
* ``adispatch(event_id, event=None)``: Trigger an event asynchronously
* ``get_listeners(event_id=None)``: Retrieve registered listeners
* ``has_listeners(event_id=None)``: Check if listeners are registered

See also :doc:`synchronous` for the sync equivalent.
