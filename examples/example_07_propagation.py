"""
Event propagation control.

This example demonstrates how to stop event propagation, preventing
remaining listeners from executing. Useful for validation or error handling.
"""

from whistle import EventDispatcher


def main():
    """Demonstrate stopping event propagation."""
    dispatcher = EventDispatcher()

    # Validator that may stop propagation
    def validate_data(event):
        print("Validating data...")
        # Simulate validation failure
        if not hasattr(event, "valid") or not event.valid:
            print("Validation failed! Stopping propagation.")
            event.stop_propagation()
        else:
            print("Validation passed")

    # This will only run if validation passes
    def process_data(event):
        print("Processing data...")

    # This will also only run if validation passes
    def save_data(event):
        print("Saving data...")

    # Register listeners in order
    dispatcher.add_listener("data.submit", validate_data)
    dispatcher.add_listener("data.submit", process_data)
    dispatcher.add_listener("data.submit", save_data)

    # First dispatch: validation fails, propagation stops
    print("=== Attempting to submit invalid data ===")
    from whistle import Event

    invalid_event = Event()
    invalid_event.valid = False
    dispatcher.dispatch("data.submit", invalid_event)

    print("\n=== Attempting to submit valid data ===")
    valid_event = Event()
    valid_event.valid = True
    dispatcher.dispatch("data.submit", valid_event)


if __name__ == "__main__":
    main()
