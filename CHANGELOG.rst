=========
Changelog
=========

All notable changes to this project are documented in this file.

The format is based on `Keep a Changelog
<https://keepachangelog.com/en/1.1.0/>`_, and this project adheres to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
==========

Added
-----

- Python 3.14 to the CI and release test matrices.
- ``Event.reset()`` to clear propagation state and allow re-dispatching the
  same event instance.

Changed
-------

- Moved the package trove classifiers into ``pyproject.toml`` so they ship in
  the published metadata, covering Python 3.10 to 3.14.
- Updated the supported Python version range in ``docs/release.rst``.

Removed
-------

- ``classifiers.txt``, which was not read by the build.
