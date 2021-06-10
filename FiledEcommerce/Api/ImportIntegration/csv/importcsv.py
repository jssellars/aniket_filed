import json
from datetime import datetime, timezone
from io import StringIO

import pandas

from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.utils.models.filed_model import FiledCustomProperties, FiledProduct, FiledVariant


class ImportCsv(Ecommerce):

    @classmethod
    def mapper(cls, data, mapping):
        """
        Mapping of csv data to Filed's models
        @param data: products from csv file
        @param mapping: mapped headers from FE
        @return: list of prodcuts with correct mapping
        """
        csv_product_list = []
        imported_at = datetime.now(timezone.utc).replace(
            microsecond=0).isoformat()[:-6] + 'Z'

        # fetch the respective headers for product and variant
        product_lst = [p['name'] for p in mapping['mapping']['product']]
        variant_lst = [v['name'] for v in mapping['mapping']['variant']]
        product_lst.extend(variant_lst)

        df = pandas.DataFrame.from_records(data)

        # get a dict of the csv column name and the mapping key
        product_dict = {dict_map["name"]: dict_map["mapped_to"] for dict_map in mapping["mapping"]['product']}
        variant_dict = {res_dict["name"]: res_dict["mapped_to"] for res_dict in mapping["mapping"]['variant']}
        merge_pv_dict = {**product_dict, **variant_dict}

        # rename the csv headers with filed model fields
        new_df = df.rename(index=str, columns=merge_pv_dict)
        # drop empty columns
        new_df.dropna(axis='columns', how='all', inplace=True)
        # fill empty rows with data of previous row based on the id. Replace NaN with ""
        new_df.update(new_df.groupby('product_id').ffill().fillna(""))

        variant_attrs = ["variant_id", "filed_product_id", "display_name", "price",
                         "compare_at_price", "availability", "url", "image_url",
                         "sku", "barcode", "inventory_quantity", "tags",
                         "description", "created_at", "updated_at", "imported_at",
                         "material", "condition", "brand", "color", "size"]
        # get a list of custom properties
        custom_fields = [
            attr
            for attr in mapping["mapping"]["variant"]
            if attr["filed_key"] not in variant_attrs
        ]

        # loop through the df and update the model
        for row in new_df.itertuples(index=False, name='FiledTuple'):
            product_attrs = FiledProduct(
                product_id=getattr(row, 'product_id', ""),
                title=getattr(row, 'title', ""),
                product_type=getattr(row, 'product_type', ""),
                description=getattr(row, 'description', ""),
                vendor=getattr(row, 'vendor', ""),
                tags=getattr(row, 'tags', ""),
                image_url=getattr(row, 'image_url', ""),
                availability=getattr(row, 'image_url', ""),
                sku="",
                created_at=getattr(row, 'created_at', imported_at),
                updated_at="",
                imported_at=imported_at,
                brand="",
                variants=[]
            )

            variant_attrs = FiledVariant(
                variant_id=getattr(row, 'variant_id', ""),
                filed_product_id=getattr(row, 'filed_product_id', ""),
                price=getattr(row, 'price', 0),
                compare_at_price=getattr(row, 'compare_at_price', 0),
                availability=getattr(row, 'availability', ""),
                url=getattr(row, 'url', ""),
                display_name=getattr(row, 'display_name', ""),
                image_url=getattr(row, 'image_url', ""),
                sku=getattr(row, 'sku', ""),
                barcode=getattr(row, 'barcode', ""),
                inventory_quantity=getattr(row, 'inventory_quantity', ""),
                tags=getattr(row, 'tags', ""),
                description=getattr(row, 'description', ""),
                created_at=getattr(row, 'created_at', imported_at),
                updated_at="",
                imported_at=imported_at,
                material=getattr(row, 'material', ""),
                condition=getattr(row, 'condition', ""),
                color=getattr(row, 'color', ""),
                size=getattr(row, 'size', ""),
                custom_props=FiledCustomProperties(
                    properties={}
                )
            )

            if custom_fields:
                custom_attrs = FiledCustomProperties(
                    properties={},
                )
            for field in custom_fields:
                custom_attrs.properties[field["name"]] = row._asdict()[
                    field["filed_key"]]
            # convert to 'str' from main
            custom_attrs = json.dumps(custom_attrs.__dict__)

            variant_attrs.custom_props = custom_attrs
            product_attrs.variants.append(variant_attrs.__dict__)
            csv_product_list.append(product_attrs.__dict__)

        return {"products": csv_product_list}

    @classmethod
    def get_products(cls, body):
        """
        Get all products from csv
        @param body: csv form-data
        @return: <generator>
        """
        file = body["file"]
        file_decode = b''.join(file).decode('utf-8')
        data = StringIO(file_decode)
        df = pandas.read_csv(data)
        df.dropna(axis='columns', how='all', inplace=True)
        product_list = df.to_dict('records')

        yield product_list
