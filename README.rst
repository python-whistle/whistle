Whistle
=======

`Whistle` is a lightweight python library that allow your application components to communicate with each other by
dispatching events and listening to them.

.. image:: https://img.shields.io/pypi/v/whistle.svg
    :target: https://pypi.org/project/whistle/
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/whistle
    :target: https://pypi.org/project/whistle/
    :alt: Python Versions

.. image:: https://github.com/python-whistle/whistle/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/python-whistle/whistle/actions/workflows/ci.yml
    :alt: CI Status

.. image:: https://img.shields.io/github/license/python-whistle/whistle
    :target: https://github.com/python-whistle/whistle/blob/main/LICENSE
    :alt: License

* Homepage: https://python-whistle.github.io/
* Issues: https://github.com/python-whistle/whistle/issues


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


----

Made with ♥ by `Romain Dorgueil <https://twitter.com/rdorgueil>`_ and `contributors <https://github.com/python-whistle/whistle/graphs/contributors>`_.


