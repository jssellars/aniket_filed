import pytest

from FacebookPixels.Api.app import app


@pytest.fixture()
def client():
    return app.test_client()
