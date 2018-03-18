Whistle
=======

`Whistle` is a lightweight python library that allow your application components to communicate with each other by
dispatching events and listening to them.

.. image:: https://img.shields.io/pypi/v/whistle.svg
    :target: https://pypi.python.org/pypi/whistle
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/whistle.svg
    :target: https://pypi.python.org/pypi/whistle
    :alt: Versions

.. image:: https://readthedocs.org/projects/whistle/badge/?version=latest
    :target: http://whistle.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/python-whistle/whistle.svg?branch=master
    :target: https://travis-ci.org/python-whistle/whistle

.. image:: https://img.shields.io/coveralls/python-whistle/whistle/master.svg
    :target: https://coveralls.io/github/python-whistle/whistle?branch=master
    :alt: Coverage

.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpython-whistle%2Fwhistle.svg?type=shield
    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fpython-whistle%2Fwhistle?ref=badge_shield
    :alt: License Status

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

.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpython-whistle%2Fwhistle.svg?type=large
    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fpython-whistle%2Fwhistle?ref=badge_large
    :alt: License Status


