import os

import jwt


def add_bearer_token(token, headers=None):
    if not headers:
        headers = {}
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json"
    return headers


def generate_technical_token(startup):
    technical_token_cache = startup.technical_token_cache
    token = technical_token_cache.get_token(startup)
    return token


def auth_jwt_base(token):
    try:
        jwt_secret_key = os.environ[
            "JWT_SECRET_KEY"] if "JWT_SECRET_KEY" in os.environ.keys() else "79f4b7c8ff6c919a5c0efc23c7b5f47975ec0d11cef5016a42422521cb62929d32690d8c3b8751dca49c61c0623763c5e5fb98382cf96b85d788fe2638ffbf12"
        payload = jwt.decode(token, jwt_secret_key)
        return payload["BusinessOwnerFacebookId"]
    except jwt.ExpiredSignatureError:
        raise ConnectionRefusedError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        return ConnectionRefusedError('Invalid token. Please log in again.')
