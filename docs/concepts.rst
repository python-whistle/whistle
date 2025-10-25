Concepts
========

Understanding Whistle's building blocks.

Events
------

An **event** represents something that happened in your application.

Events have:

* A **name** (string like ``"user.login"`` or ``"order.completed"``)
* Optional **data** (carried by the event object)
* A **dispatcher** reference (set automatically)

Example event names::

    user.registered
    order.placed
    payment.received
    system.startup

Listeners
---------

A **listener** is a function that responds to an event. When an event is dispatched, all registered listeners for that event are called.

Listeners can:

* Read event data
* Perform actions (send emails, log messages, update databases)
* Modify the event object
* Stop propagation

Synchronous dispatchers require regular functions. Asynchronous dispatchers require async functions.

Dispatcher
----------

The **dispatcher** is the central hub that:

* Maintains which listeners subscribe to which events
* Manages listener priorities and execution order
* Dispatches events to registered listeners
* Enforces type safety (sync vs async)

Whistle provides two implementations:

* ``EventDispatcher`` - For synchronous operations
* ``AsyncEventDispatcher`` - For asynchronous operations

Priorities
----------

**Priorities** control listener execution order. Lower numbers execute first.

* **Default**: 0 (normal priority)
* **High priority**: Negative numbers (e.g., -10)
* **Low priority**: Positive numbers (e.g., 10)

Use priorities to:

* Run validation before processing
* Ensure logging happens early
* Control workflow order

Event Propagation
-----------------

**Event propagation** is the flow of an event through registered listeners. By default, all listeners execute in priority order.

Any listener can **stop propagation** by calling ``event.stop_propagation()``:

* Current listener completes
* Remaining listeners are skipped
* Dispatcher returns normally (no exception)

Use this for:

* Validation failures
* Authorization checks
* Early returns when conditions are met
