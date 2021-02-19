import pytest
import jwt

from FacebookCampaignsBuilder.Api.app import app

BUSINESS_OWNER_ID = "1623950661230875"
ACCOUNT_ID = "act_389109158588065"
SECRET_KEY = "dummy-key"

PAYLOAD = {
    "jti": "69360ad6-3560-4f6c-ba5e-141663acc5b5",
    "sub": "dev-test@filed.com",
    "user_filed_id": "3",
    "user_firstname": "Andrew",
    "user_lastname": "G",
    "user_account_state": "1",
    "user_is_frontoffice_user": "True",
    "permissions_filed": "01^3|02^f|03^f|1E^3|1F^1ff|82^7c02|96^3|A0^1|A1^1ff|B4^7fffff|BE^3ff",
    "user_facebook_businessowner_id": BUSINESS_OWNER_ID,
    "exp": 1617460349,
    "iss": "Filed-Token-Issuer",
    "aud": "Filed-Client-Apps",
}


@pytest.fixture(scope="session")
def client():
    return app.test_client()


@pytest.fixture(scope="session")
def config():
    encoded_jwt = jwt.encode(payload=PAYLOAD, key=SECRET_KEY).decode("UTF-8")
    headers = {"Authorization": f"Bearer {encoded_jwt}"}

    return {"business_owner_id": BUSINESS_OWNER_ID, "account_id": ACCOUNT_ID, "headers": headers}
