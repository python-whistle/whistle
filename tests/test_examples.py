"""
Test suite for documentation examples.

These tests ensure that all example code in the documentation works correctly.
Following TDD principles, these tests are written first, then examples are implemented to pass them.
"""

from io import StringIO
from unittest import mock


class TestBasicExamples:
    """Test basic synchronous examples."""

    def test_01_basic_sync(self):
        """Test basic synchronous dispatcher example."""
        from examples import example_01_basic_sync

        # Should run without errors
        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_01_basic_sync.main()
            output = mock_stdout.getvalue()

        # Should print something (event was dispatched)
        assert len(output) > 0

    def test_02_sync_multiple_listeners(self):
        """Test synchronous example with multiple listeners."""
        from examples import example_02_sync_multiple_listeners

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_02_sync_multiple_listeners.main()
            output = mock_stdout.getvalue()

        # Should show multiple listeners executed
        assert len(output.splitlines()) >= 2

    def test_03_sync_decorator(self):
        """Test synchronous example using @listen decorator."""
        from examples import example_03_sync_decorator

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_03_sync_decorator.main()
            output = mock_stdout.getvalue()

        # Should show decorator-registered listener executed
        assert len(output) > 0


class TestAsyncExamples:
    """Test asynchronous examples."""

    async def test_04_basic_async(self):
        """Test basic asynchronous dispatcher example."""
        from examples import example_04_basic_async

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            await example_04_basic_async.main()
            output = mock_stdout.getvalue()

        # Should print something (async event was dispatched)
        assert len(output) > 0

    async def test_05_async_io_operations(self):
        """Test async example with I/O operations."""
        from examples import example_05_async_io_operations

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            await example_05_async_io_operations.main()
            output = mock_stdout.getvalue()

        # Should show async operations completed
        assert len(output) > 0


class TestAdvancedExamples:
    """Test advanced feature examples."""

    def test_06_priorities(self):
        """Test priority system example."""
        from examples import example_06_priorities

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_06_priorities.main()
            output = mock_stdout.getvalue()

        lines = output.splitlines()
        # Should show listeners executed in priority order
        assert len(lines) >= 3

        # Verify priority order (high priority listeners run first)
        # High priority should appear before low priority in output
        output_str = " ".join(lines)
        high_pos = output_str.find("high")
        low_pos = output_str.find("low")
        if high_pos >= 0 and low_pos >= 0:
            assert high_pos < low_pos, "High priority should execute before low priority"

    def test_07_propagation(self):
        """Test event propagation control example."""
        from examples import example_07_propagation

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_07_propagation.main()
            output = mock_stdout.getvalue()

        # Should show some listeners executed, but not all (propagation stopped)
        assert len(output) > 0

    def test_08_custom_event(self):
        """Test custom event class example."""
        from examples import example_08_custom_event

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_08_custom_event.main()
            output = mock_stdout.getvalue()

        # Should show custom event data being used
        assert len(output) > 0

    def test_09_listener_management(self):
        """Test listener management operations example."""
        from examples import example_09_listener_management

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_09_listener_management.main()
            output = mock_stdout.getvalue()

        # Should demonstrate has_listeners, get_listeners, remove_listener
        assert len(output) > 0


class TestPatternExamples:
    """Test common pattern examples."""

    def test_10_patterns(self):
        """Test common patterns example."""
        from examples import example_10_patterns

        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            example_10_patterns.main()
            output = mock_stdout.getvalue()

        # Should demonstrate multiple patterns
        assert len(output) > 0
        # Should show different pattern sections
        assert len(output.splitlines()) >= 4
