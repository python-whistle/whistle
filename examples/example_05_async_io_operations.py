"""
Asynchronous event dispatching with I/O operations.

This example shows how AsyncEventDispatcher is useful for coordinating
async operations like database writes, API calls, or file I/O.
"""

import asyncio

from whistle import AsyncEventDispatcher


async def main():
    """Demonstrate async event dispatching with simulated I/O operations."""
    dispatcher = AsyncEventDispatcher()

    # Simulate async database write
    async def save_to_database(event):
        print("Saving to database...")
        await asyncio.sleep(0.02)  # Simulate I/O delay
        print("Database save complete")

    # Simulate async API call
    async def notify_external_service(event):
        print("Notifying external service...")
        await asyncio.sleep(0.01)  # Simulate network delay
        print("External service notified")

    # Register async listeners
    dispatcher.add_listener("order.created", save_to_database)
    dispatcher.add_listener("order.created", notify_external_service)

    # Dispatch event - listeners execute sequentially with async/await
    print("Order created, processing...")
    await dispatcher.adispatch("order.created")
    print("All async operations complete")


if __name__ == "__main__":
    asyncio.run(main())
