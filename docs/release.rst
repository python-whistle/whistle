Release Process
===============

This document describes the process for releasing a new version of Whistle.

Prerequisites
-------------

Before releasing, ensure you have:

* Push access to the GitHub repository
* All changes merged to the ``main`` branch
* All tests passing on CI

The release process is fully automated via GitHub Actions. You only need to create and push a git tag.

Release Steps
-------------

1. **Ensure everything is ready**

   Run tests locally to verify everything works:

   .. code-block:: bash

      make test
      make format

2. **Set the version number**

   Define the version number in an environment variable to avoid typos:

   .. code-block:: bash

      export VERSION=2.0.2
      # Or for a release candidate:
      export VERSION=2.1.0-rc1

3. **Update version in pyproject.toml**

   Update the version in ``pyproject.toml`` and commit the change:

   .. code-block:: bash

      # Update the version in pyproject.toml (cross-platform)
      sed -i.bak "s/^version = .*/version = \"$VERSION\"/" pyproject.toml && rm pyproject.toml.bak

      # Commit the version change
      git add pyproject.toml
      git commit -m "chore: bump version to $VERSION"

      # Push to main
      git push origin main

4. **Create an annotated git tag**

   Create an annotated tag (required for proper git object tracking):

   .. code-block:: bash

      git tag -a $VERSION -m "Release $VERSION"

   The ``-a`` flag creates an annotated tag (a real git object with metadata).
   The ``-m`` flag provides a message for the tag.

5. **Push the tag to GitHub**

   .. code-block:: bash

      git push origin $VERSION

6. **GitHub Actions takes over**

   Once the tag is pushed, the Release workflow automatically:

   * Builds the Python package (wheel and sdist)
   * Tests the package on Python 3.10-3.13
   * Publishes to TestPyPI
   * Publishes to PyPI
   * Creates a GitHub Release with the built artifacts

7. **Monitor the release**

   Watch the GitHub Actions workflow at:
   https://github.com/python-whistle/whistle/actions

   The workflow typically takes 5-10 minutes to complete.

8. **Verify the release**

   Once complete, verify the release:

   * Check PyPI: https://pypi.org/project/whistle/
   * Check GitHub Releases: https://github.com/python-whistle/whistle/releases
   * Test installation: ``pip install whistle==$VERSION``

Version Naming
--------------

Follow semantic versioning:

* **Stable releases**: ``X.Y.Z`` (e.g., ``2.0.2``, ``2.1.0``)
* **Release candidates**: ``X.Y.Z-rcN`` (e.g., ``2.1.0-rc1``)
* **Beta releases**: ``X.Y.Z-betaN`` (e.g., ``2.1.0-beta1``)
* **Alpha releases**: ``X.Y.Z-alphaN`` (e.g., ``2.1.0-alpha1``)

Pre-release versions (rc, beta, alpha) are automatically marked as pre-releases on GitHub.

Complete Example
----------------

Here's a complete example of releasing version 2.0.2:

.. code-block:: bash

   # Set version
   export VERSION=2.0.2

   # Run tests
   make test
   make format

   # Update version in pyproject.toml
   sed -i.bak "s/^version = .*/version = \"$VERSION\"/" pyproject.toml && rm pyproject.toml.bak
   git add pyproject.toml
   git commit -m "chore: bump version to $VERSION"
   git push origin main

   # Create and push annotated tag
   git tag -a $VERSION -m "Release $VERSION"
   git push origin $VERSION

   # Verify after GitHub Actions completes
   pip install whistle==$VERSION

Troubleshooting
---------------

**Release workflow fails**

1. Check the GitHub Actions logs for errors
2. Fix any issues in the code
3. Delete the failed tag both locally and on GitHub:

   .. code-block:: bash

      export VERSION=2.0.2  # Set to the failed version
      git tag -d $VERSION
      git push origin :refs/tags/$VERSION

4. Create and push the tag again after fixing issues

**PyPI credentials issues**

The release workflow uses GitHub's trusted publishing (OIDC). No manual credentials are needed.
If publishing fails, verify the PyPI trusted publisher configuration at:
https://pypi.org/manage/account/publishing/

Manual Build (Testing)
----------------------

To test the build process locally without publishing:

.. code-block:: bash

   make wheel

This creates distribution files in the ``dist/`` directory using an isolated sandbox environment.

Emergency Rollback
------------------

If a release has critical issues:

1. **Do not delete the PyPI release** (PyPI does not allow re-uploading the same version)
2. Instead, release a new patch version with the fix
3. Optionally mark the problematic release as yanked on PyPI (prevents new installs but doesn't break existing ones)

For yanking a release on PyPI:

1. Go to https://pypi.org/project/whistle/
2. Select the problematic version
3. Click "Options" → "Yank release"
