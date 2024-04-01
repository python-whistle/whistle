from unittest.mock import AsyncMock, Mock

import pytest
from pytest import fixture

from whistle import AsyncEventDispatcher, EventDispatcher


class BaseDispatcherTest:
    @fixture
    def dispatcher(self):
        raise NotImplementedError()

    def create_handler(self):
        raise NotImplementedError()

    def create_invalid_handler(self):
        raise NotImplementedError()

    def test_dispatch_invalid(self, dispatcher):
        handler = self.create_invalid_handler()
        with pytest.raises(TypeError):
            dispatcher.add_listener("test", handler)


class TestAsyncDispatcher(BaseDispatcherTest):
    @fixture
    def dispatcher(self):
        return AsyncEventDispatcher()

    def create_handler(self):
        return AsyncMock()

    def create_invalid_handler(self):
        return Mock()

    def test_dispatch(self, dispatcher):
        handler = self.create_handler()
        dispatcher.add_listener("test", handler)
        with pytest.raises(NotImplementedError):
            dispatcher.dispatch("test")

    async def test_adispatch(self, dispatcher):
        handler = self.create_handler()
        dispatcher.add_listener("test", handler)
        await dispatcher.adispatch("test")
        assert handler.called


class TestSyncDispatcher(BaseDispatcherTest):
    @fixture
    def dispatcher(self):
        return EventDispatcher()

    def create_handler(self):
        return Mock()

    def create_invalid_handler(self):
        return AsyncMock()

    def test_dispatch(self, dispatcher):
        handler = self.create_handler()
        dispatcher.add_listener("test", handler)
        dispatcher.dispatch("test")
        assert handler.called

    async def test_adispatch(self, dispatcher):
        handler = self.create_handler()
        dispatcher.add_listener("test", handler)
        await dispatcher.adispatch("test")
        assert handler.called
