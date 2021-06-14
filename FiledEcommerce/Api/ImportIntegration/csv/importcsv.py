import json
from datetime import datetime, timezone
from io import StringIO

import numpy as np
import pandas
from sqlalchemy import select

from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.utils.models.filed_model import FiledCustomProperties, FiledProduct, FiledVariant
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import engine, cols, external_platforms


class ImportCsv(Ecommerce):

    @classmethod
    def pre_install(cls):
        pass

    @classmethod
    def app_install(cls):
        pass

    @classmethod
    def app_load(cls):
        pass

    @classmethod
    def app_uninstall(cls):
        pass

    @classmethod
    def mapper(cls, data, mapping):
        """
        Mapping of csv data to Filed's models
        @param data: products from csv file
        @param mapping: mapped headers from FE
        @return: list of products with correct mapping
        """
        filed_product_list = []
        imported_at = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat()[:-6] + 'Z'

        for csv_p in data:
            df = {}
            for p_map in mapping["mapping"].get('product'):
                if p_map["filed_key"] in FiledProduct.__annotations__:
                    df[p_map['filed_key']] = csv_p[p_map["mapped_to"]]

            filed_product = FiledProduct(
                product_id=df.get("product_id"),
                title=df.get("title"),
                product_type=df.get("product_type"),
                vendor=df.get("vendor"),
                description=df.get("description"),
                tags=", ".join([df.get("tags")]) if df["tags"] != 0 else "",
                sku=df.get("sku"),
                image_url=df.get("image_url"),
                created_at=csv_p.get("created_at", imported_at),
                updated_at=csv_p.get("updated_at", imported_at),
                imported_at=imported_at,
                variants=[],
                brand=df.get("brand"),
                availability=df.get("availability", ""),
            )

            variant_map = {"custom_fields": {}}
            for v_map in mapping["mapping"].get('variant'):
                if v_map["filed_key"] in FiledVariant.__annotations__:
                    variant_map[v_map['filed_key']] = csv_p[v_map["mapped_to"]]
                else:
                    custom = {v_map["filed_key"]: csv_p.get(v_map["mapped_to"])}
                    variant_map["custom_fields"].update(custom)

            filed_variant = FiledVariant(
                variant_id=variant_map.get("variant_id", ""),
                filed_product_id="",
                display_name=filed_product.title,
                price=variant_map.get("price", ""),
                compare_at_price=variant_map.get("compare_at_price", ""),
                availability=variant_map.get("availability", ""),
                url=variant_map.get("url", ""),
                image_url=variant_map.get("url", ""),
                sku=variant_map.get("sku", ""),
                barcode=variant_map.get("barcode", ""),
                inventory_quantity=variant_map.get("inventory_quantity", ""),
                tags=filed_product.tags,
                description=variant_map.get("description", ""),
                created_at=csv_p.get("created_at", imported_at),
                updated_at=csv_p.get("updated_at", imported_at),
                imported_at=imported_at,
                material="",
                condition="",
                color="",
                size="",
                custom_props=FiledCustomProperties(
                    properties=variant_map["custom_fields"]
                ) if variant_map["custom_fields"] else None,
            )
            filed_product.variants.append(filed_variant.__dict__)
            filed_product_list.append(filed_product.__dict__)

        return {"products": filed_product_list}

    @classmethod
    def get_products(cls, body):
        """
        Get all products from csv
        @param body: csv form-data
        @return: <generator>
        """
        file = body["file"]
        user_id = body["user_filed_id"]
        file_decode = b''.join(file).decode('utf-8')
        data = StringIO(file_decode)
        df = pandas.read_csv(data)
        # df.dropna(axis='columns', how='all', inplace=True)
        df1 = df.replace(np.nan, '', regex=True)
        product_list = df1.to_dict('records')
        details = {
            "user_id": user_id
        }
        cls.write_to_db(details, body)

        yield product_list

    @staticmethod
    def write_to_db(details: dict, data):
        user_id = data.get("user_filed_id")
        flag = 0
        with engine.connect() as conn:
            query = (
                select([cols.Name])
                    .where(cols.FiledBusinessOwnerId == user_id)
                    .limit(1)
            )
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

        with engine.connect() as conn:
            ins = external_platforms.insert().values(
                CreatedAt=datetime.now(),
                CreatedById=user_id,
                CreatedByFirstName=user_first_name,
                CreatedByLastName=user_last_name,
                FiledBusinessOwnerId=user_id,
                PlatformId=7,
                Details=json.dumps(details),
            )
            result = conn.execute(ins)
