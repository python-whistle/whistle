Whistle - Event Dispatcher
===========================

**Whistle** is a lightweight Python library for decoupled application communication through event dispatching and listening. It enables components to interact without direct dependencies, making your code more modular, testable, and maintainable.

.. code-block:: python

    from whistle import EventDispatcher

    dispatcher = EventDispatcher()

    @dispatcher.listen("user.registered")
    def send_welcome_email(event):
        print(f"Welcome, {event.username}!")

    dispatcher.dispatch("user.registered")

Features
--------

* **Synchronous and asynchronous dispatching** - Choose the right dispatcher for your use case
* **Priority-based listener execution** - Control the order listeners run
* **Event propagation control** - Stop event flow when needed
* **Type safety** - Prevent mixing sync and async listeners
* **Custom events** - Attach domain-specific data to events
* **Zero dependencies** - Lightweight and easy to integrate

Learning Path
-------------

Follow this guide to learn Whistle from basics to advanced usage:

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   introduction
   installation
   getting_started
   concepts
   patterns

.. toctree::
   :maxdepth: 1
   :caption: Core Features

   synchronous
   asynchronous
   priorities
   propagation

.. toctree::
   :maxdepth: 1
   :caption: Advanced Usage

   custom_events
   listener_management
   recipes

.. toctree::
   :maxdepth: 1
   :caption: Reference

   release
   reference/whistle

Quick Links
-----------

* :doc:`getting_started` - Start here if you're new
* :doc:`recipes` - Common recipes and best practices
* :doc:`reference/whistle` - Complete API documentation
* `GitHub Repository <https://github.com/python-whistle/whistle>`_
* `PyPI Package <https://pypi.org/project/whistle/>`_

Indices and tables
::::::::::::::::::

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

