Listener Priorities
===================

When multiple listeners are registered for the same event, priorities control their execution order.

Understanding Priorities
-------------------------

Priorities are integers that determine execution order:

* **Lower numbers execute first** (higher priority)
* **Higher numbers execute last** (lower priority)
* **Default priority**: 0 (normal priority)

Priority Range
--------------

* **Permitted range**: -127 to 128 (inclusive)
* **Recommended convention**: -20 (highest) to 20 (lowest)
* **Default**: 0

The full range is available for technical reasons (performance optimization with string keys), but the -20 to 20 convention is recommended for clarity and consistency.

Priority Example
----------------

Here's an example showing priority-based execution:

.. literalinclude:: ../examples/example_06_priorities.py
    :language: python

Running this produces::

    Starting system...
    1. High priority task (priority=-10)
    2. Normal priority task (priority=0, default)
    3. Low priority task (priority=10)
    System started

Notice how listeners execute in ascending priority order, regardless of registration order.

Common Priority Patterns
------------------------

Validation First
~~~~~~~~~~~~~~~~

Use high priority (negative numbers) for validation::

    @dispatcher.listen("data.submit", priority=-10)
    def validate(event):
        if not event.is_valid:
            event.stop_propagation()  # Prevent processing

    @dispatcher.listen("data.submit", priority=0)
    def process(event):
        # Only runs if validation passes
        ...

Logging and Metrics
~~~~~~~~~~~~~~~~~~~

Use very high priority for observability::

    @dispatcher.listen("*", priority=-20)
    def log_all_events(event):
        logger.info(f"Event: {event.name}")

    @dispatcher.listen("*", priority=-15)
    def track_metrics(event):
        metrics.increment(f"events.{event.name}")

Cleanup and Finalization
~~~~~~~~~~~~~~~~~~~~~~~~~

Use low priority (positive numbers) for cleanup::

    @dispatcher.listen("request.complete", priority=10)
    def cleanup_resources(event):
        event.connection.close()

    @dispatcher.listen("request.complete", priority=15)
    def send_telemetry(event):
        telemetry.send(event.stats)

Priority Best Practices
------------------------

1. **Use the convention range** (-20 to 20) for clarity
2. **Reserve extreme priorities** (-20, 20) for cross-cutting concerns
3. **Use default (0)** for most business logic
4. **Document priorities** when they matter for correctness
5. **Avoid fine-grained priorities** unless necessary (stick to increments of 5 or 10)

Same Priority
-------------

When multiple listeners have the same priority, they execute in **registration order**::

    dispatcher.add_listener("event", first_listener, priority=0)
    dispatcher.add_listener("event", second_listener, priority=0)
    dispatcher.add_listener("event", third_listener, priority=0)

    # Execution order: first_listener, second_listener, third_listener

This behavior is deterministic and can be relied upon.

Priorities with Decorators
---------------------------

The ``@listen`` decorator accepts a ``priority`` parameter::

    @dispatcher.listen("event.name", priority=-5)
    def high_priority_listener(event):
        ...

    @dispatcher.listen("event.name", priority=5)
    def low_priority_listener(event):
        ...

See also :doc:`propagation` to learn how to stop event flow.
