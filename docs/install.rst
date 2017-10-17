Quick start
===========

Installation
::::::::::::

.. code-block:: shell-session

    $ pip install whistle

Quick start
:::::::::::

.. code-block:: python

    from whistle import Event, EventDispatcher

    class HelloWorldEvent(Event):
        pass

    dispatcher = EventDispatcher()




