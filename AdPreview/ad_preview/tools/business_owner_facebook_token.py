import pyodbc
from adpreview.config import DATABASE_CONFIG
from adpreview.config import USER_TOKEN_CONNECTION_STRING

__GET_USER_TOKEN__ = """SELECT TOP(1) token FROM FacebookUserTokens WHERE FacebookUserTokens.user_id = '{user_id}'"""


def get_user_token(business_owner_facebook_id=None):
    assert business_owner_facebook_id is not None

    connection_string = USER_TOKEN_CONNECTION_STRING.format(driver=DATABASE_CONFIG['driver'],
                                                            server=DATABASE_CONFIG['server'],
                                                            database=DATABASE_CONFIG['database'],
                                                            username=DATABASE_CONFIG['username'],
                                                            password=DATABASE_CONFIG['password'])
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    query = __GET_USER_TOKEN__.format(user_id=business_owner_facebook_id)
    results = [r[0] for r in cursor.execute(query)]

    if results:
        return results[0]
    else:
        return None
