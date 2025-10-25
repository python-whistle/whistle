Common Patterns
===============

This section demonstrates practical patterns for using event dispatchers in real-world applications.

Complete Example
----------------

The following example demonstrates multiple common patterns:

.. literalinclude:: ../examples/example_10_patterns.py
    :language: python
    :lines: 8-

Running this produces::

    === Pattern 1: Conditional Dispatch ===
    Optional handler executed
    Event dispatched

    === Pattern 2: Plugin Architecture ===
    [LOG] Event: *
    [METRICS] Tracking: *
    [BUSINESS] Handling: *

    === Pattern 3: Event-Driven Workflow ===
    Step 1: Validating order
    Step 2: Charging payment
    Step 3: Shipping order

    === Pattern 4: Audit Logging ===
    [AUDIT] User 42 performed: delete
    [COMPLIANCE] Flagged action: delete

Pattern 1: Conditional Dispatch
--------------------------------

Check if listeners exist before expensive operations::

    if dispatcher.has_listeners("optional.event"):
        # Only create expensive event object if needed
        event = ExpensiveEvent(compute_data())
        dispatcher.dispatch("optional.event", event)

**Use when:**

* Event creation is expensive (database queries, file I/O)
* Events are optional (debugging, metrics)
* You want to optimize performance

Pattern 2: Plugin Architecture
-------------------------------

Build extensible applications where plugins register event listeners::

    class Plugin:
        """Base plugin interface."""
        def register(self, dispatcher):
            raise NotImplementedError

    class LoggingPlugin(Plugin):
        def register(self, dispatcher):
            dispatcher.add_listener("*", self.log, priority=-20)

        def log(self, event):
            logger.info(f"Event: {event.name}")

    # Load plugins
    plugins = [LoggingPlugin(), MetricsPlugin(), CachePlugin()]
    for plugin in plugins:
        plugin.register(dispatcher)

**Use when:**

* Building extensible applications
* Supporting third-party extensions
* Need to enable/disable features dynamically

Pattern 3: Event-Driven Workflow
---------------------------------

Coordinate multi-step workflows using events and priorities::

    @dispatcher.listen("order.process", priority=-10)
    def validate(event):
        event.validated = True

    @dispatcher.listen("order.process", priority=0)
    def charge(event):
        if event.validated:
            event.charged = True

    @dispatcher.listen("order.process", priority=10)
    def fulfill(event):
        if event.charged:
            event.fulfilled = True

**Use when:**

* Coordinating complex workflows
* Steps have dependencies
* Need clear separation of concerns

Pattern 4: Audit Logging
-------------------------

Track actions across your application::

    class AuditEvent(Event):
        def __init__(self, user_id, action, resource=None):
            self.user_id = user_id
            self.action = action
            self.resource = resource
            self.timestamp = datetime.now()

    @dispatcher.listen("audit.log", priority=-20)
    def write_audit_log(event):
        database.insert_audit_log(
            user_id=event.user_id,
            action=event.action,
            resource=event.resource,
            timestamp=event.timestamp
        )

    # Use throughout application
    dispatcher.dispatch("audit.log",
        AuditEvent(user_id=current_user.id, action="delete", resource="document"))

**Use when:**

* Need comprehensive audit trails
* Compliance requirements (GDPR, HIPAA)
* Security monitoring

Pattern 5: Request/Response
----------------------------

Use events for request/response patterns::

    class QueryEvent(Event):
        def __init__(self, query):
            self.query = query
            self.results = []

        def add_result(self, result):
            self.results.append(result)

    @dispatcher.listen("search.query")
    def search_database(event):
        results = database.search(event.query)
        event.add_result(results)

    @dispatcher.listen("search.query")
    def search_cache(event):
        results = cache.search(event.query)
        event.add_result(results)

    # Dispatch and collect results
    event = QueryEvent("python")
    dispatcher.dispatch("search.query", event)
    all_results = event.results

**Use when:**

* Collecting data from multiple sources
* Aggregating results
* Implementing provider patterns

Pattern 6: Error Handling
--------------------------

Centralize error handling with events::

    class ErrorEvent(Event):
        def __init__(self, exception, context):
            self.exception = exception
            self.context = context
            self.handled = False

    @dispatcher.listen("error.occurred", priority=-20)
    def log_error(event):
        logger.error(f"Error: {event.exception}", exc_info=event.exception)

    @dispatcher.listen("error.occurred", priority=-10)
    def notify_admin(event):
        if isinstance(event.exception, CriticalError):
            email.send_admin_alert(event.exception, event.context)

    @dispatcher.listen("error.occurred")
    def mark_handled(event):
        event.handled = True

    # Use in error handling
    try:
        dangerous_operation()
    except Exception as e:
        event = ErrorEvent(e, context={"user": current_user})
        dispatcher.dispatch("error.occurred", event)
        if not event.handled:
            raise

**Use when:**

* Centralizing error handling
* Need multiple error handlers
* Want consistent error logging

Pattern 7: Feature Flags
-------------------------

Control features with event listeners::

    class FeatureManager:
        def __init__(self, dispatcher):
            self.dispatcher = dispatcher
            self.enabled_features = set()

        def enable(self, feature_name, listener):
            if feature_name not in self.enabled_features:
                self.dispatcher.add_listener(
                    f"feature.{feature_name}",
                    listener
                )
                self.enabled_features.add(feature_name)

        def disable(self, feature_name, listener):
            if feature_name in self.enabled_features:
                self.dispatcher.remove_listener(
                    f"feature.{feature_name}",
                    listener
                )
                self.enabled_features.discard(feature_name)

    # Use feature flags
    features = FeatureManager(dispatcher)
    features.enable("new_ui", render_new_ui)
    features.disable("new_ui", render_new_ui)

**Use when:**

* Gradual rollouts
* A/B testing
* Temporary features

Pattern 8: State Machine
-------------------------

Implement state transitions with events::

    class StateMachine:
        def __init__(self, dispatcher):
            self.dispatcher = dispatcher
            self.state = "initial"

        def transition(self, new_state):
            old_state = self.state
            event = StateChangeEvent(old_state, new_state)

            self.dispatcher.dispatch(f"state.exit.{old_state}", event)
            if event.propagation_stopped:
                return False  # Transition denied

            self.state = new_state
            self.dispatcher.dispatch(f"state.enter.{new_state}", event)
            return True

    class StateChangeEvent(Event):
        def __init__(self, old_state, new_state):
            self.old_state = old_state
            self.new_state = new_state

    # Define state handlers
    @dispatcher.listen("state.exit.draft")
    def on_exit_draft(event):
        if not validate_document():
            event.stop_propagation()  # Prevent transition

    @dispatcher.listen("state.enter.published")
    def on_enter_published(event):
        notify_subscribers()

**Use when:**

* Implementing workflows with states
* Need validation before transitions
* Want hooks for state changes

Best Practices
--------------

1. **Keep listeners focused**: Each listener should do one thing
2. **Use priorities wisely**: Reserve extreme priorities for infrastructure
3. **Document event contracts**: Specify what data events carry
4. **Handle propagation carefully**: Only stop when necessary
5. **Consider performance**: Check ``has_listeners()`` for expensive events
6. **Test listener order**: Ensure priority-dependent logic works correctly
7. **Clean up listeners**: Remove listeners when components are destroyed

See also the :doc:`reference/whistle` for the complete API reference.
