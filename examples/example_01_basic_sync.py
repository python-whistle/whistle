"""
Basic synchronous event dispatching example.

This example demonstrates the simplest use case: creating a dispatcher,
registering a listener, and dispatching an event.
"""

from whistle import EventDispatcher


def main():
    """Demonstrate basic synchronous event dispatching."""
    # Create an event dispatcher
    dispatcher = EventDispatcher()

    # Define a listener function
    def on_spectacle_starts(event):
        print("Please turn down your phones!")

    # Register the listener for a specific event
    dispatcher.add_listener("spectacle.starts", on_spectacle_starts)

    # Dispatch the event
    dispatcher.dispatch("spectacle.starts")


if __name__ == "__main__":
    main()
