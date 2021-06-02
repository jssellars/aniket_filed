woocommerce_mapping = {
    "mapping": {
        "product": [
            {"name": "id", "filedKey": "product_id", "mappedTo": "product_id", "type": "string", "disabled": True},
            {"name": "name", "filedKey": "title", "mappedTo": "title", "type": "string", "disabled": True},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": True},
            {
                "name": "type",
                "filedKey": "product_type",
                "mappedTo": "product_type",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "description",
                "filedKey": "description",
                "mappedTo": "description",
                "type": "string",
                "disabled": False,
            },
            {"name": "tags", "filedKey": "tags", "mappedTo": "tags", "type": "string", "disabled": False},
        ],
        "variant": [
            {
                "name": "image",
                "filedKey": "image_url",
                "mappedTo": "image_url",
                "type": "string",
                "disabled": True,
            },
            {
                "name": "description",
                "filedKey": "description",
                "mappedTo": "description",
                "type": "string",
                "disabled": False,
            },
            {"name": "sale_price", "filedKey": "price", "mappedTo": "price", "type": "string", "disabled": False},
            {
                "name": "stock_quantity",
                "filedKey": "inventory_quantity",
                "mappedTo": "inventory_quantity",
                "type": "string",
                "disabled": False,
            },
            {"name": "permalink", "filedKey": "url", "mappedTo": "url", "type": "string", "disabled": False},
            {"name": "sku", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": False},
        ],
    }
}
