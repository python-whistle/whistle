"""
Common patterns and recipes.

This example demonstrates several common patterns for using event dispatchers
in real-world applications.
"""

from whistle import Event, EventDispatcher


def main():
    """Demonstrate common event dispatcher patterns."""

    # Pattern 1: Conditional Dispatch (check before dispatching)
    print("=== Pattern 1: Conditional Dispatch ===")
    dispatcher = EventDispatcher()

    @dispatcher.listen("optional.event")
    def optional_handler(event):
        print("Optional handler executed")

    # Only dispatch if listeners are registered
    if dispatcher.has_listeners("optional.event"):
        dispatcher.dispatch("optional.event")
        print("Event dispatched")
    else:
        print("No listeners, skipping dispatch")

    # Pattern 2: Plugin Architecture
    print("\n=== Pattern 2: Plugin Architecture ===")

    class Plugin:
        """Base plugin class."""

        def register(self, dispatcher):
            """Register plugin's event listeners."""
            raise NotImplementedError

    class LoggingPlugin(Plugin):
        """Plugin that logs events."""

        def register(self, dispatcher):
            dispatcher.add_listener("*", self.log_event, priority=-20)

        def log_event(self, event):
            print(f"[LOG] Event: {event.name}")

    class MetricsPlugin(Plugin):
        """Plugin that tracks metrics."""

        def register(self, dispatcher):
            dispatcher.add_listener("*", self.track_metric, priority=-10)

        def track_metric(self, event):
            print(f"[METRICS] Tracking: {event.name}")

    # Set up plugins
    app_dispatcher = EventDispatcher()
    plugins = [LoggingPlugin(), MetricsPlugin()]

    for plugin in plugins:
        plugin.register(app_dispatcher)

    # All plugins respond to all events
    @app_dispatcher.listen("*")
    def business_logic(event):
        print(f"[BUSINESS] Handling: {event.name}")

    app_dispatcher.dispatch("*")

    # Pattern 3: Event-Driven Workflow
    print("\n=== Pattern 3: Event-Driven Workflow ===")
    workflow_dispatcher = EventDispatcher()

    @workflow_dispatcher.listen("order.placed", priority=-10)
    def validate_order(event):
        print("Step 1: Validating order")
        event.validated = True

    @workflow_dispatcher.listen("order.placed", priority=0)
    def charge_payment(event):
        if getattr(event, "validated", False):
            print("Step 2: Charging payment")
            event.paid = True

    @workflow_dispatcher.listen("order.placed", priority=10)
    def ship_order(event):
        if getattr(event, "paid", False):
            print("Step 3: Shipping order")

    workflow_event = Event()
    workflow_dispatcher.dispatch("order.placed", workflow_event)

    # Pattern 4: Audit Logging
    print("\n=== Pattern 4: Audit Logging ===")
    audit_dispatcher = EventDispatcher()

    class AuditEvent(Event):
        """Event with audit information."""

        def __init__(self, user_id, action):
            self.user_id = user_id
            self.action = action

    @audit_dispatcher.listen("audit.log", priority=-20)
    def write_audit_log(event):
        print(f"[AUDIT] User {event.user_id} performed: {event.action}")

    @audit_dispatcher.listen("audit.log")
    def send_compliance_report(event):
        if event.action in ["delete", "modify"]:
            print(f"[COMPLIANCE] Flagged action: {event.action}")

    audit_event = AuditEvent(user_id=42, action="delete")
    audit_dispatcher.dispatch("audit.log", audit_event)


if __name__ == "__main__":
    main()
