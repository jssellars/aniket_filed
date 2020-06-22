import os

from string import Template

FACEBOOK_CONFIG = {
    "__class": "FacebookConfig",
    "description": "Filed",
    "api_version": "v5.0",
    "app_id": "174014546372191",
    "app_secret": "718ab2ca9cc128cf4b1b7793ecc116cb",
    "business_owner_facebook_id": "1623950661230875",
    'ad_account_id': 'act_2066904460189854',
    "permanent_token": 'EAABsbCS1iHgBAPfLaUZBVNyGBBq7rBVCLKQRifi6MBTiH3qXrtv1NpRwHpLcQqeRMEPwXOA8XZCoycKuyYS1AvPeUAvUqJQTsZBHw6EqtRZBxAKNHTHDe1ZAwIR0KmTW14GUS2GQqgEH8XZC4OYUTZAXZBKwfyHBA0tVwHfMt31Qz7ZBUH51JDt5ZARgcSMQUarg0ZD'
}

USER_TOKEN_CONNECTION_STRING = """Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};"""

env = os.environ.get('PYTHON_ENV', None)
if env == 'dev' or env is None:
    DATABASE_CONFIG = {
        "driver": 'SQL Server',
        "server": "filed-dev-database-instance.cjjxmuvqxehb.eu-west-2.rds.amazonaws.com",
        "port": 1433,
        "username": "admin",
        "password": "F2!irf0q",
        "database": "filed-facebook-tokens"
    }
elif env == 'dev2':
    DATABASE_CONFIG = {
        "driver": 'SQL Server',
        "server": "dev2.filed.com",
        "port": 1433,
        "username": "sa",
        "password": "Parola@20",
        "database": "Dev2.Filed.Facebook.Potter.Accounts"
    }
elif env == 'prod':
    DATABASE_CONFIG = {
        "driver": 'SQL Server',
        "server": "35.176.246.229",
        "port": 1433,
        "username": "tempsa",
        "password": "KoalaBearSplitsaStair",
        "database": "Prod.Filed.Facebook.Potter.Accounts"
    }

FACEBOOK_SEARCH_URL = "https://graph.facebook.com/{api_version}/{ad_account_id}/targetingsearch?q={search_input}&access_token={token}&limit=5000"
SUGGEST_INTEREST_URL = "https://graph.facebook.com/{api_version}/search?interest_list={interests}&type=adinterestsuggestion&access_token={token}&limit=5000"

AUDIENCE_DETAILS_URL = Template(
    'https://graph.facebook.com/v5.0/$adAccountFacebookId/delivery_estimate?access_token=$accessTokenFacebook&attribution_spec=$attributionSpec&bid_strategy=$bidStrategy&currency=$currency&optimization_goal=$optimizationGoal&targeting_spec=$targetingSpec')
