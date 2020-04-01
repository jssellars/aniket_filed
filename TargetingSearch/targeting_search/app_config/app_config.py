FACEBOOK_CONFIG = {
    "__class": "FacebookConfig",
    "description": "Filed",
    "api_version": "v5.0",
    "app_id": "174014546372191",
    "app_secret": "718ab2ca9cc128cf4b1b7793ecc116cb",
    "business_owner_facebook_id": "1623950661230875",
    'ad_account_id': 'act_2066904460189854',
    "permanent_token": "EAACvp5II9r0BAHkWxpaJKE9kwpTo7mgo3c7TIWUI8DCTLCXX8c4JQMwVV9NKqtAfNHbdIRr3Ix4U727IWeGomAXKlp4DhQz9ZCMGe2ANdtAt2SZCPE28GC5e40k5YZAuaOmxB1A2sWVcwUmZBBZAHmkJsOZBn5s6g8ZAhqqT8WUCcyQ5APon7iQZC8ULhXoLHHQZD"
}

USER_TOKEN_CONNECTION_STRING = """Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};"""

DATABASE_CONFIG = {
    "driver": 'SQL Server',
    "server": "filed-dev-database-instance.cjjxmuvqxehb.eu-west-2.rds.amazonaws.com",
    "port": 1433,
    "username": "admin",
    "password": "F2!irf0q",
    "database": "filed-facebook-tokens"
}

FACEBOOK_SEARCH_URL = "https://graph.facebook.com/{api_version}/{ad_account_id}/targetingsearch?q={search_input}&access_token={token}&limit=5000"
SUGGEST_INTEREST_URL = "https://graph.facebook.com/{api_version}/search?interest_list={interests}&type=adinterestsuggestion&access_token={token}&limit=5000"

AUDIENCE_DETAILS_URL = "https://graph.facebook.com/{api_version}/{ad_account_id}/delivery_estimate?access_token={token}"+\
    "&targeting_spec={targeting_spec}&optimization_goal={optimization_goal}&attribution_spec={attribution_spec}&bid_strategy={bid_strategy}"
