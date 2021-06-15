from facebook_business.adobjects.productitem import ProductItem as FacebookProductItem
                 
facebook_mapping = {
    "mapping": {
        "variants": [
            {
                "name": "ID",
                "filedKey": "Id",
                "mappedTo": FacebookProductItem.Field.id,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Currency",
                "filedKey": "CurrencyId",
                "mappedTo": FacebookProductItem.Field.currency, 
                "type": "string",
                "disabled": False
            },
            {
                "name": "Short Description",
                "filedKey": "ShortDescription",
                "mappedTo": FacebookProductItem.Field.description,
                "type": "string",
                "disabled": True,
            },
            {
                "name": "Url",
                "filedKey": "Url",
                "mappedTo": FacebookProductItem.Field.url,
                "type": "string",
                "disabled": True,
            },
            {
                "name": "Availability",
                "filedKey": "Availability",
                "mappedTo": FacebookProductItem.Field.availability,
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Name",
                "filedKey": "Name",
                "mappedTo": FacebookProductItem.Field.name,
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Price",
                "filedKey": "Price",
                "mappedTo": FacebookProductItem.Field.price,
                "type": "string",
                "disabled": False
            },
            {
                "name": "ProductType",
                "filedKey": "ProductType",
                "mappedTo": FacebookProductItem.Field.product_group,
                "type": "string",
                "disabled": False
            },
            {
                "name": "ProductType",
                "filedKey": "ProductType",
                "mappedTo": FacebookProductItem.Field.category,
                "type": "string",
                "disabled": False,
            },
                   {
                "name": "ProductType",
                "filedKey": "ProductType",
                "mappedTo": FacebookProductItem.Field.product_type,
                "type": "string",
                "disabled": False,
            },
            {
                "name": "ShortDescription",
                "filedKey": "ShortDescription",
                "mappedTo": FacebookProductItem.Field.short_description,
                "type": "string",
                "disabled": False
            },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.custom_data,
            #     "type": "string",
            #     "disabled": False
            # },
            {
                "name": "Tags",
                "filedKey": "Tags",
                "mappedTo": FacebookProductItem.Field.custom_label_0,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Tags",
                "filedKey": "Tags",
                "mappedTo": FacebookProductItem.Field.custom_label_1,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Tags",
                "filedKey": "Tags",
                "mappedTo":  FacebookProductItem.Field.custom_label_2,
                "type": "string",
                "disabled": False
            },

            {
                "name": "Tags",
                "filedKey": "Tags",
                "mappedTo":  FacebookProductItem.Field.custom_label_3,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Tags",
                "filedKey": "Tags",
                "mappedTo":  FacebookProductItem.Field.custom_label_4,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Additional Images",
                "filedKey": "CustomImages",
                "mappedTo": FacebookProductItem.Field.additional_image_urls,
                "type": "string",
                "disabled": False
            },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo":  FacebookProductItem.Field.additional_variant_attributes,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo":   FacebookProductItem.Field.age_group,
            #     "type": "string",
            #     "disabled": False
            # },
            {
                "name": "ImageUrl",
                "filedKey": "ImageUrl",
                "mappedTo": FacebookProductItem.Field.image_url,
                "type": "string",
                "disabled": False
            },
            {
                "name": "ImageUrl",
                "filedKey": "ImageUrl",
                "mappedTo": FacebookProductItem.Field.image_cdn_urls,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Gender",
                "filedKey": "Gender",
                "mappedTo": FacebookProductItem.Field.gender,
                "type": "string",
                "disabled": False
            },
            # {
            #     "name": "Brand",
            #     "filedKey": "Brand",
            #     "mappedTo":  FacebookProductItem.Field.brand,
            #     "type": "string",
            #     "disabled": False
            # },
            {
                "name": "Color",
                "filedKey": "Color",
                "mappedTo": FacebookProductItem.Field.color,
                "type": "string",
                "disabled": False
            },
            {
                "name": "Condition",
                "filedKey": "Condition",
                "mappedTo": FacebookProductItem.Field.condition,
                "type": "string",
                "disabled": False
            },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.expiration_date,
            #     "type": "string",
            #     "disabled": False
            # },
            {
                "name": "InventoryQuantity",
                "filedKey": "InventoryQuantity",
                "mappedTo": FacebookProductItem.Field.inventory,
                "type": "int",
                "disabled": False
            },
            {
                "name": "Material",
                "filedKey": "Material",
                "mappedTo": FacebookProductItem.Field.material,
                "type": "string",
                "disabled": False
            },

            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo":FacebookProductItem.Field.pattern,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.retailer_product_group_id,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.review_status,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.review_rejection_reasons,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.sale_price,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.sale_price_end_date,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.sale_price_start_date,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.shipping_weight_unit,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.shipping_weight_value,
            #     "type": "string",
            #     "disabled": False
            # },
            {
                "name": "Size",
                "filedKey": "Size",
                "mappedTo": FacebookProductItem.Field.size,
                "type": "string",
                "disabled": False
            },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.offer_price_amount,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.offer_price_end_date,
            #     "type": "string",
            #     "disabled": False
            # },
            # {
            #     "name": "SKU",
            #     "filedKey": "sku",
            #     "mappedTo": FacebookProductItem.Field.offer_price_start_date,
            #     "type": "string",
            #     "disabled": False
            # },
        ],
    }
}
