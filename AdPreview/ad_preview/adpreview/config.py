import os


class FacebookConfig(object):
    __class = "FacebookConfig"
    description = "Filed Live"
    api_version = "v5.0"
    app_id = "174014546372191"
    app_secret = "718ab2ca9cc128cf4b1b7793ecc116cb"
    user_id = "1623950661230875"
    permanent_token = "EAACeQZBs45l8BACaZCOWQeKSCyJEMOZALZBhD1Y9ZAerAmdd4y5asiB1aF0pmYiYb4ENNiSZBtA8h7LzdMp3Pzxe3D5IuzK4jPgim5ZBOYvAdwLpNSYQWUimsqCjIGdEQW8P5e07SzGuDd2WZC1NdEEQZCIOENwGaR78rAfe9tZAJuBi1zpJvBxpnjRDzmzEgOi8kZD"


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
elif env == 'staging':
    DATABASE_CONFIG = {
        "driver": 'SQL Server',
        "server": "dev2.filed.com",
        "port": 1433,
        "username": "sa",
        "password": "Parola@20",
        "database": "Staging.Filed.Facebook.Potter.Accounts"
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
