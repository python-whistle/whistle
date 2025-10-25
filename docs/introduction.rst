Introduction
============

What is Whistle?
----------------

**Whistle** is a lightweight Python library for event-driven communication between application components. It enables loose coupling through event dispatching and listening.

The Problem
-----------

When components call each other directly, they become tightly coupled. This makes code harder to test, modify, and extend.

The Solution
------------

Whistle introduces an intermediary - the event dispatcher:

* Components **publish events** when something happens
* Other components **listen** to events they care about
* The **dispatcher** routes events to registered listeners
* Components stay independent and decoupled

This enables:

* Adding features without modifying existing code
* Testing components in isolation
* Flexible plugin systems
* Clean separation of concerns

When to Use Whistle
-------------------

Event dispatchers are useful for:

* Plugin and extension systems
* Workflow orchestration
* Audit logging and notifications
* Decoupling business logic from cross-cutting concerns
