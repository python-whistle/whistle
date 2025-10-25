"""
Listener management and introspection.

This example demonstrates how to check for listeners, retrieve them,
and remove them when needed.
"""

from whistle import EventDispatcher


def main():
    """Demonstrate listener management operations."""
    dispatcher = EventDispatcher()

    def listener_one(event):
        print("Listener one executed")

    def listener_two(event):
        print("Listener two executed")

    # Check if event has listeners before registering
    print("=== Initial State ===")
    print(f"Has listeners for 'app.start': {dispatcher.has_listeners('app.start')}")

    # Register listeners
    dispatcher.add_listener("app.start", listener_one)
    dispatcher.add_listener("app.start", listener_two)

    print("\n=== After Registration ===")
    print(f"Has listeners for 'app.start': {dispatcher.has_listeners('app.start')}")

    # Get all listeners for an event
    listeners = dispatcher.get_listeners("app.start")
    print(f"Number of listeners: {len(listeners)}")

    # Dispatch event
    print("\n=== Dispatching Event ===")
    dispatcher.dispatch("app.start")

    # Remove a listener
    print("\n=== After Removing listener_two ===")
    dispatcher.remove_listener("app.start", listener_two)
    print(f"Number of listeners: {len(dispatcher.get_listeners('app.start'))}")

    # Dispatch again - only listener_one executes
    print("\n=== Dispatching Event Again ===")
    dispatcher.dispatch("app.start")

    # Check if any events have listeners (v1.x compatibility)
    print("\n=== Global Check ===")
    print(f"Dispatcher has any listeners: {dispatcher.has_listeners()}")


if __name__ == "__main__":
    main()
