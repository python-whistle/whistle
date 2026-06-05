class Event(object):
    """
    Base class to represent whistle's events. You can subclass this if you want to embed special data and associated
    logic with your events, or just let the event dispatcher create instances for you

    The event handlers will have :class:`Event` instances passed, so you can bundle any data required by your handlers
    there.

    """

    name = None
    """Event name placeholder, will be set by dispatcher."""

    dispatcher = None

    propagation_stopped = False
    """Has the event propagation ended?"""

    def stop_propagation(self):
        """Stop event propagation, meaning that the remaining handlers won't be called after this one."""
        self.propagation_stopped = True

    def reset(self):
        """
        Reset the propagation state so the same event instance can be dispatched again.

        Useful when a single event instance is reused across several dispatches and an intermediate
        listener stopped propagation in a previous run.
        """
        self.propagation_stopped = False
