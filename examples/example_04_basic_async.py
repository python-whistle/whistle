"""
Basic asynchronous event dispatching.

This example demonstrates async/await usage with AsyncEventDispatcher.
All listeners must be async functions (coroutines).
"""

import asyncio

from whistle import AsyncEventDispatcher


async def main():
    """Demonstrate basic asynchronous event dispatching."""
    # Create an async event dispatcher
    dispatcher = AsyncEventDispatcher()

    # Define an async listener function
    async def on_data_received(event):
        # Simulate async operation
        await asyncio.sleep(0.01)
        print(f"Data received for event: {event.name}")

    # Register the async listener
    dispatcher.add_listener("data.received", on_data_received)

    # Dispatch the event asynchronously
    await dispatcher.adispatch("data.received")


if __name__ == "__main__":
    asyncio.run(main())
