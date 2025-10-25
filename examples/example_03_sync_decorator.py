"""
Using the @listen decorator for cleaner listener registration.

This example demonstrates the decorator pattern for registering listeners,
which provides a more elegant syntax.
"""

from whistle import EventDispatcher


def main():
    """Demonstrate listener registration using decorators."""
    dispatcher = EventDispatcher()

    # Use decorator to register listeners
    @dispatcher.listen("user.login")
    def on_user_login(event):
        print(f"User logged in - event: {event.name}")

    @dispatcher.listen("user.logout")
    def on_user_logout(event):
        print(f"User logged out - event: {event.name}")

    # Dispatch events
    dispatcher.dispatch("user.login")
    dispatcher.dispatch("user.logout")


if __name__ == "__main__":
    main()
