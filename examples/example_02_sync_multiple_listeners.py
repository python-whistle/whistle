"""
Multiple listeners for a single event.

This example shows how multiple listeners can respond to the same event,
executing in the order they were registered (when no priority is specified).
"""

from whistle import EventDispatcher


def main():
    """Demonstrate multiple listeners for a single event."""
    dispatcher = EventDispatcher()

    # Define multiple listener functions
    def turn_off_lights(event):
        print("1. Turning off the lights")

    def start_music(event):
        print("2. Starting the music")

    def open_curtains(event):
        print("3. Opening the curtains")

    # Register all listeners for the same event
    dispatcher.add_listener("show.start", turn_off_lights)
    dispatcher.add_listener("show.start", start_music)
    dispatcher.add_listener("show.start", open_curtains)

    # Dispatch the event - all listeners will be called
    dispatcher.dispatch("show.start")


if __name__ == "__main__":
    main()
