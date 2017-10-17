class Event(object):
    """
    Base class to represent whistle's events. You can subclass this if you want to embed special data and associated
    logic with your events, or just let the event dispatcher create instances for you

    The event handlers will have :class:`Event` instances passed, so you can bundle any data required by your handlers
    there.

    """

    propagation_stopped = False
    """Has the event propagation ended?"""

    def stop_propagation(self):
        """Stop event propagation, meaning that the remaining handlers won't be called after this one."""
        self.propagation_stopped = True
