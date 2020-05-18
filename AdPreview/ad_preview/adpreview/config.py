class FacebookConfig(object):
    __class = "FacebookConfig"
    description = "Filed Live"
    api_version = "v5.0"
    app_id = "174014546372191"
    app_secret = "718ab2ca9cc128cf4b1b7793ecc116cb"
    user_id = "1623950661230875"
    permanent_token = "EAACeQZBs45l8BACaZCOWQeKSCyJEMOZALZBhD1Y9ZAerAmdd4y5asiB1aF0pmYiYb4ENNiSZBtA8h7LzdMp3Pzxe3D5IuzK4jPgim5ZBOYvAdwLpNSYQWUimsqCjIGdEQW8P5e07SzGuDd2WZC1NdEEQZCIOENwGaR78rAfe9tZAJuBi1zpJvBxpnjRDzmzEgOi8kZD"


USER_TOKEN_CONNECTION_STRING = """Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};"""

DATABASE_CONFIG = {
    "driver": 'ODBC Driver 17 for SQL Server',
    "server": "dev.filed.com",
    "username": "sa",
    "password": "Parola@20",
    "database": "Facebook.Potter.FacebookAccounts"
}
