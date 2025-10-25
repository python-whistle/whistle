Custom Event Classes
====================

While the base ``Event`` class works for simple cases, you can create custom event classes to carry domain-specific data and behavior.

Why Custom Events?
------------------

Custom event classes provide:

* **Type safety**: IDEs can autocomplete event attributes
* **Documentation**: Event structure is explicit in code
* **Validation**: Ensure required data is present
* **Behavior**: Add methods for common event operations
* **Clarity**: Domain concepts are clearly represented

Creating Custom Events
-----------------------

Subclass ``Event`` and add your own attributes and methods:

.. literalinclude:: ../examples/example_08_custom_event.py
    :language: python
    :lines: 8-28

The custom event class:

* Inherits from ``Event`` to get ``stop_propagation()`` and other base functionality
* Adds domain-specific attributes (``user_id``, ``username``, ``email``)
* Provides custom methods (``get_display_name()``)

Using Custom Events
-------------------

Create instances and dispatch them:

.. literalinclude:: ../examples/example_08_custom_event.py
    :language: python
    :lines: 31-49

Running this produces::

    Sending welcome email to alice@example.com
      User: alice (alice@example.com)
      ID: 12345
    New user registered: alice

Listeners can access all custom attributes and methods on the event object.

Custom Event Patterns
----------------------

Rich Domain Events
~~~~~~~~~~~~~~~~~~

Include all relevant domain data::

    class OrderPlacedEvent(Event):
        def __init__(self, order_id, customer_id, items, total):
            self.order_id = order_id
            self.customer_id = customer_id
            self.items = items
            self.total = total

        def get_item_count(self):
            return sum(item.quantity for item in self.items)

        def requires_shipping(self):
            return any(item.physical for item in self.items)

Validation Events
~~~~~~~~~~~~~~~~~

Carry validation state::

    class DataValidationEvent(Event):
        def __init__(self, data):
            self.data = data
            self.errors = []
            self.warnings = []

        def add_error(self, message):
            self.errors.append(message)
            self.stop_propagation()  # Stop on error

        def add_warning(self, message):
            self.warnings.append(message)

        def is_valid(self):
            return len(self.errors) == 0

Workflow Events
~~~~~~~~~~~~~~~

Track workflow state::

    class WorkflowEvent(Event):
        def __init__(self, workflow_id):
            self.workflow_id = workflow_id
            self.completed_steps = []
            self.current_step = None

        def mark_step_complete(self, step_name):
            self.completed_steps.append(step_name)

        def has_completed(self, step_name):
            return step_name in self.completed_steps

Event Inheritance
-----------------

Create event hierarchies for related events::

    class BaseUserEvent(Event):
        """Base class for all user-related events."""
        def __init__(self, user_id):
            self.user_id = user_id

    class UserRegisteredEvent(BaseUserEvent):
        def __init__(self, user_id, email):
            super().__init__(user_id)
            self.email = email

    class UserDeletedEvent(BaseUserEvent):
        def __init__(self, user_id, reason):
            super().__init__(user_id)
            self.reason = reason

This allows listeners to handle specific events or all events in a hierarchy.

Immutable Events
----------------

Consider making events immutable for safety::

    class ImmutableOrderEvent(Event):
        def __init__(self, order_id, total):
            self._order_id = order_id
            self._total = total

        @property
        def order_id(self):
            return self._order_id

        @property
        def total(self):
            return self._total

This prevents listeners from accidentally modifying event data.

Best Practices
--------------

1. **Keep events focused**: One event per domain concept
2. **Include all relevant data**: Listeners shouldn't need to query for more info
3. **Make events immutable** when possible to prevent unintended modifications
4. **Document event structure**: Docstrings should explain all attributes
5. **Use type hints**: Help IDEs and type checkers understand your events
6. **Provide helper methods**: Add convenience methods for common operations

Example with Type Hints
------------------------

::

    from typing import List
    from whistle import Event

    class ProductUpdatedEvent(Event):
        """Event dispatched when a product is updated.

        Attributes:
            product_id: Unique product identifier
            changes: List of field names that changed
            old_values: Dictionary of old values for changed fields
            new_values: Dictionary of new values for changed fields
        """

        def __init__(
            self,
            product_id: int,
            changes: List[str],
            old_values: dict,
            new_values: dict
        ):
            self.product_id = product_id
            self.changes = changes
            self.old_values = old_values
            self.new_values = new_values

        def was_field_changed(self, field_name: str) -> bool:
            """Check if a specific field was changed."""
            return field_name in self.changes

See also :doc:`patterns` for examples using custom events.
