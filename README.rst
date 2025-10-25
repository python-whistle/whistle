Whistle
=======

A lightweight, pure-Python event dispatcher for building decoupled applications.

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

**Key Features:**

* 🚀 **Pure Python** - No external dependencies
* 🔄 **Sync & Async** - Full support for both synchronous and asynchronous workflows
* 🎯 **Type Safe** - Prevents mixing sync and async listeners
* 📦 **Lightweight** - Minimal footprint, maximum flexibility
* 🎛️ **Priority Control** - Order listener execution
* ⚡ **Event Propagation** - Stop event flow when needed

Installation
::::::::::::

.. code-block:: shell

   pip install whistle

Requires Python 3.10 or later. No dependencies.

Quick Start
:::::::::::

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


Documentation
:::::::::::::

For complete documentation, visit https://python-whistle.github.io/

Links
:::::

* Homepage: https://python-whistle.github.io/
* Documentation: https://python-whistle.github.io/
* PyPI: https://pypi.org/project/whistle/
* Source Code: https://github.com/python-whistle/whistle
* Issue Tracker: https://github.com/python-whistle/whistle/issues

----

Made with ♥ by Romain Dorgueil and `contributors <https://github.com/python-whistle/whistle/graphs/contributors>`_.


