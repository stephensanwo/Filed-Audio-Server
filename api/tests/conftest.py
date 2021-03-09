import pytest

from api import api


@pytest.fixture
def app():
    yield api


@pytest.fixture
def client(app):
    return app.test_client()
