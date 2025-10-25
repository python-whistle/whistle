"""
Custom event classes.

This example demonstrates creating custom Event subclasses to carry
domain-specific data and behavior.
"""

from whistle import Event, EventDispatcher


class UserRegisteredEvent(Event):
    """Custom event for user registration with domain data."""

    def __init__(self, user_id, username, email):
        """Initialize event with user data."""
        self.user_id = user_id
        self.username = username
        self.email = email

    def get_display_name(self):
        """Custom method on the event."""
        return f"{self.username} ({self.email})"


def main():
    """Demonstrate custom event classes."""
    dispatcher = EventDispatcher()

    # Listener that accesses custom event data
    def send_welcome_email(event):
        print(f"Sending welcome email to {event.email}")
        print(f"  User: {event.get_display_name()}")
        print(f"  ID: {event.user_id}")

    def log_registration(event):
        print(f"New user registered: {event.username}")

    # Register listeners
    dispatcher.add_listener("user.registered", send_welcome_email)
    dispatcher.add_listener("user.registered", log_registration)

    # Create and dispatch custom event
    event = UserRegisteredEvent(user_id=12345, username="alice", email="alice@example.com")
    dispatcher.dispatch("user.registered", event)


if __name__ == "__main__":
    main()
