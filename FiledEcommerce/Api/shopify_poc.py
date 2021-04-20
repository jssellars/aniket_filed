import requests


def shopify_data_receiver(username, password, shop_name, endpoint, resource_url=None):
    api_version = "2021-04"
    base_url = f"https://{username}:{password}@{shop_name}.myshopify.com/admin/api/{api_version}/{endpoint}"

    if resource_url:
        shopify_request_url = f"{base_url}/{resource_url}.json"
    else:
        shopify_request_url = f"{base_url}.json"
    data = requests.get(shopify_request_url)
    if data.status_code == 200:
        return {"status": True, "data": data.json()}
    else:
        return {"status": False, "data": data.json()}
