import pymssql

from app_config.app_config import DATABASE_CONFIG

__GET_USER_TOKEN__ = """SELECT TOP(1) token FROM BusinessOwners WHERE BusinessOwners.facebook_id = '{user_id}'"""


def get_user_token(business_owner_facebook_id=None):
    assert business_owner_facebook_id is not None

    conn = pymssql.connect(server=DATABASE_CONFIG['server'],
                           port=str(DATABASE_CONFIG['port']),
                           user=DATABASE_CONFIG['username'],
                           password=DATABASE_CONFIG['password'],
                           database=DATABASE_CONFIG['database'])
    cursor = conn.cursor()
    query = __GET_USER_TOKEN__.format(user_id=business_owner_facebook_id)
    cursor.execute(query)
    results = [r[0] for r in cursor.fetchall()]

    cursor.close()
    conn.close()
    if results:
        return results[0]
    else:
        return None
