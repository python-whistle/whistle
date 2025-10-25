"""
Listener priority system.

This example demonstrates how to control the execution order of listeners
using priorities. Lower priority numbers execute first (higher priority).

Priority range: -127 to 128
Convention: -20 (highest) to 20 (lowest), default is 0
"""

from whistle import EventDispatcher


def main():
    """Demonstrate listener execution order with priorities."""
    dispatcher = EventDispatcher()

    # Register listeners with different priorities
    @dispatcher.listen("system.startup", priority=10)
    def low_priority_task(event):
        print("3. Low priority task (priority=10)")

    @dispatcher.listen("system.startup", priority=0)
    def normal_priority_task(event):
        print("2. Normal priority task (priority=0, default)")

    @dispatcher.listen("system.startup", priority=-10)
    def high_priority_task(event):
        print("1. High priority task (priority=-10)")

    # Dispatch the event - listeners execute in priority order
    print("Starting system...")
    dispatcher.dispatch("system.startup")
    print("System started")


if __name__ == "__main__":
    main()
