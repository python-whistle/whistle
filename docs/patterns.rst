Design Patterns
===============

Whistle implements two well-established design patterns to enable decoupled communication between components.

Observer Pattern
----------------

The `Observer pattern <https://en.wikipedia.org/wiki/Observer_pattern>`_ defines a one-to-many dependency where multiple observers (listeners) are notified when a subject (event) changes state.

In Whistle:

* **Subject**: Events dispatched through the dispatcher
* **Observers**: Listener functions registered for specific events
* **Notification**: The dispatcher calls all registered listeners when an event is dispatched

This pattern allows components to react to changes without knowing about each other.

Mediator Pattern
----------------

The `Mediator pattern <https://en.wikipedia.org/wiki/Mediator_pattern>`_ uses an intermediary object to control communication between components, preventing them from referring to each other directly.

In Whistle:

* **Mediator**: The EventDispatcher or AsyncEventDispatcher
* **Colleagues**: Components that dispatch events or listen to them
* **Decoupling**: Components interact only with the dispatcher, not each other

This pattern reduces coupling by centralizing complex communications and control between objects.

Why Both Patterns?
------------------

Whistle combines these patterns:

* The **Observer pattern** defines how listeners subscribe and react to events
* The **Mediator pattern** defines how the dispatcher coordinates between components

Together, they enable flexible, maintainable communication in your applications.
