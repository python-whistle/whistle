"""Version information for whistle package."""

try:
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("whistle")
except PackageNotFoundError:
    # Fallback for development/editable installs
    __version__ = "unknown"
