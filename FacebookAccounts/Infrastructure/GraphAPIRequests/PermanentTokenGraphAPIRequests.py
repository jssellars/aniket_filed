def get_exchange_temporary_token_url(temporary_token, config):
    return (
        f"https://graph.facebook.com/{config.facebook.api_version}/oauth/access_token"
        f"?grant_type=fb_exchange_token"
        f"&client_id={config.facebook.app_id}"
        f"&client_secret={config.facebook.app_secret}"
        f"&fb_exchange_token={temporary_token}"
    )


def get_generate_permanent_token_url(business_owner_facebook_id, exchanged_token, config):
    return (
        f"https://graph.facebook.com/{config.facebook.api_version}/{business_owner_facebook_id}/accounts"
        f"?access_token={exchanged_token}"
    )


def get_delete_permissions_url(business_owner_facebook_id, business_owner_permanent_token, config):
    return (
        f"https://graph.facebook.com/{config.facebook.api_version}/{business_owner_facebook_id}/permissions"
        f"&access_token={business_owner_permanent_token}"
    )
