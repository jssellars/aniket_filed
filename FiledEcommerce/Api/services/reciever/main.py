from datetime import datetime

from Core.Web.Security.JWTTools import extract_user_filed_id, decode_jwt_from_headers
from FiledEcommerce.Api.ImportIntegration.interface.ImportIntegrationProvider import ImportIntegrationProvider
from FiledEcommerce.Api.services.publisher.main import publisher_lambda
from FiledEcommerce.Api.utils.tools.json_serializer import ResponseSerializer
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import *
from FiledEcommerce.Api.utils.tools.date_utils import get_utc_aware_date

def receiver_lambda(request, platform):
    token_data = decode_jwt_from_headers()

    user_id = extract_user_filed_id()
    mapping = request["mapping"]
    request.update(token_data)

    with engine.connect() as conn:
        flag = 0
        query = select([cols.Name]).where(cols.FiledBusinessOwnerId == user_id).limit(1)
        for row in conn.execute(query):
            try:
                user_name = row[0]
                flag = 1
            except Exception as e:
                raise e
        if flag == 1:
            temp_nl = user_name.split(" ", 1)
            if len(temp_nl) == 2:
                user_first_name, user_last_name = temp_nl[0], temp_nl[1]
            else:
                user_first_name, user_last_name = temp_nl[0], ""

        filed_product_catalogs_ins = filed_product_cat.insert().values(
            CreatedAt=get_utc_aware_date(),
            CreatedById=user_id,
            CreatedByFirstName=user_first_name,
            CreatedByLastName=user_last_name,
            FiledBusinessOwnerId=user_id,
            Name=f"{platform} catalog",
            StateId=1,
            LastImportAt=get_utc_aware_date(),
        )
        result = conn.execute(filed_product_catalogs_ins)
        filed_product_catalog_id = result.inserted_primary_key

        filed_product_catalogs_permissions_ins = fpc_permissions.insert().values(
            FiledProductCatalogId=filed_product_catalog_id[0], FiledUserId=user_id, FiledBusinessOwnerId=user_id
        )
        conn.execute(filed_product_catalogs_permissions_ins)

    store = ImportIntegrationProvider.get_instance(platform)
    for idx, data in enumerate(store.get_products(request)):
        mapped_data = store.mapper(data, mapping)
        response = publisher_lambda(user_id, filed_product_catalog_id, platform, mapped_data)

    return response
