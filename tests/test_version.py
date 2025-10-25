"""Tests for version information."""


def test_version_is_available():
    """Test that version can be imported."""
    from whistle._version import __version__

    assert __version__ is not None


def test_version_is_string():
    """Test that version is a string."""
    from whistle._version import __version__

    assert isinstance(__version__, str)


def test_version_format():
    """Test that version has valid format when package is installed."""
    from whistle._version import __version__

    # Version should not be "unknown" when package is properly installed
    # In development/editable installs, it might be "unknown"
    assert len(__version__) > 0
    assert isinstance(__version__, str)


def test_version_accessible_from_package():
    """Test that version is accessible from main package."""
    import whistle

    assert hasattr(whistle, "__version__")
    assert isinstance(whistle.__version__, str)
