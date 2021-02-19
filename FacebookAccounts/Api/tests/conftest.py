import pytest
import jwt
from FacebookAccounts.Api.app import app
from Core.test_config import PAYLOAD, SECRET_KEY, BUSINESS_OWNER_ID, ACCOUNT_ID


@pytest.fixture(scope="session")
def client():
    return app.test_client()


@pytest.fixture(scope="session")
def config():
    encoded_jwt = jwt.encode(payload=PAYLOAD, key=SECRET_KEY).decode("UTF-8")
    headers = {"Authorization": f"Bearer {encoded_jwt}"}
    return {"business_owner_id": BUSINESS_OWNER_ID, "account_id": ACCOUNT_ID, "headers": headers}
