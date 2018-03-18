Whistle
=======

`Whistle` provides simple python tools that allow your application components to communicate with each other by dispatching events and listening to them.

.. image:: https://travis-ci.org/python-whistle/whistle.svg?branch=master
    :target: https://travis-ci.org/python-whistle/whistle

.. image:: https://coveralls.io/repos/github/python-whistle/whistle/badge.svg?branch=master
    :target: https://coveralls.io/github/python-whistle/whistle?branch=master
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/whistle/badge/?version=latest
    :target: http://whistle.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status


Install
:::::::

.. code-block:: shell

   pip install whistle


Quick start
:::::::::::

Install the `whistle` package:

.. code-block:: shell-session

    $ pip install whistle

Create an event dispatcher:

.. code-block:: python

    from whistle import EventDispatcher

    dispatcher = EventDispatcher()

Add a listener to react to events

.. code-block:: python

    def on_spectacle_starts(event):
        print('Please turn down your phones!')

    dispatcher.add_listener('spectacle.starts', on_spectacle_starts)</code></pre>

Dispatch!

.. code-block:: python

    dispatcher.dispatch('spectacle.starts')
