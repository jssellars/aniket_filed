import pytest

from FiledInfluencer.Api.app import app


@pytest.fixture(scope="session")
def client():
    return app.test_client()
