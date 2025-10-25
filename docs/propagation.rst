Event Propagation Control
==========================

Event propagation refers to the flow of an event through registered listeners. Any listener can stop propagation to prevent remaining listeners from executing.

Stopping Propagation
---------------------

Call ``event.stop_propagation()`` within a listener to stop event flow::

    def validator(event):
        if not event.is_valid:
            event.stop_propagation()  # Stop here

    def processor(event):
        # This won't run if validation stopped propagation
        ...

When propagation stops:

* The current listener completes normally
* All remaining listeners are skipped (in priority order)
* The dispatcher returns normally (no exception raised)

Propagation Example
-------------------

Here's a complete example showing propagation control:

.. literalinclude:: ../examples/example_07_propagation.py
    :language: python
    :lines: 8-

Running this produces::

    === Attempting to submit invalid data ===
    Validating data...
    Validation failed! Stopping propagation.

    === Attempting to submit valid data ===
    Validating data...
    Validation passed
    Processing data...
    Saving data...

Notice how validation failure prevents processing and saving in the first case.

Common Use Cases
----------------

Validation
~~~~~~~~~~

Stop processing when validation fails::

    @dispatcher.listen("form.submit", priority=-10)
    def validate_form(event):
        if not event.form.is_valid():
            event.error = "Invalid form data"
            event.stop_propagation()

    @dispatcher.listen("form.submit")
    def save_form(event):
        # Only runs if validation passed
        database.save(event.form)

Authorization
~~~~~~~~~~~~~

Deny access and prevent further processing::

    @dispatcher.listen("resource.access", priority=-20)
    def check_permission(event):
        if not user.has_permission(event.resource):
            event.denied = True
            event.stop_propagation()

    @dispatcher.listen("resource.access")
    def load_resource(event):
        # Only runs if authorization passed
        event.data = database.load(event.resource)

Early Return
~~~~~~~~~~~~

Stop when a condition is met::

    @dispatcher.listen("cache.get")
    def check_memory_cache(event):
        if event.key in memory_cache:
            event.value = memory_cache[event.key]
            event.stop_propagation()  # Found in memory, skip disk

    @dispatcher.listen("cache.get")
    def check_disk_cache(event):
        # Only runs if not found in memory
        if event.key in disk_cache:
            event.value = disk_cache[event.key]

Checking Propagation Status
----------------------------

Check if propagation was stopped::

    event = dispatcher.dispatch("event.name")

    if event.propagation_stopped:
        print("Event was stopped by a listener")
    else:
        print("Event completed normally")

This is useful for logging or metrics.

Propagation with Priorities
----------------------------

Propagation respects priority order. Only listeners that haven't executed yet are skipped::

    @dispatcher.listen("event", priority=-10)  # Executes first
    def first(event):
        print("First runs")

    @dispatcher.listen("event", priority=0)    # Executes second
    def second(event):
        print("Second runs")
        event.stop_propagation()  # Stop here

    @dispatcher.listen("event", priority=10)   # Never executes
    def third(event):
        print("Third never runs")

Output::

    First runs
    Second runs

Best Practices
--------------

1. **Stop propagation for errors**: Use it for validation failures, authorization denials, or error conditions
2. **Document stopping behavior**: Make it clear when and why a listener stops propagation
3. **Use with high priority**: Validation and authorization should run early with high priority
4. **Provide feedback**: Set properties on the event to indicate why propagation stopped
5. **Test both paths**: Ensure your code works whether propagation stops or continues

Async Propagation
-----------------

Propagation control works identically with ``AsyncEventDispatcher``::

    @async_dispatcher.listen("event")
    async def async_validator(event):
        result = await validate_async(event.data)
        if not result:
            event.stop_propagation()

See also :doc:`priorities` to learn about controlling execution order.
