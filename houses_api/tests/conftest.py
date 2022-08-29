"""Configuration for our restful API testing"""
import pytest
from api.config import TestingConfig
from api.app import create_app


@pytest.fixture
def app():
    """
    app fixture to create a testing application before each test without
    running a server each time
    """
    application = create_app(config_object=TestingConfig)
    with application.app_context():
        yield application


@pytest.fixture
# pylint: disable=redefined-outer-name
def test_client(app):
    """
    The test client makes requests to the application without running
    a live server. Flasks client extends Werkzeug client,
    see those docs for additional information.
    The client has methods that match the common HTTP request methods,
     such as client.get() and client.post().
    """
    with app.test_client() as test_client:
        yield test_client
