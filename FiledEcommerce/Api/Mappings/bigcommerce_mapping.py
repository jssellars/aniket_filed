bigcommerce_mapping = {
    "mapping": {
        "product": [
            {"name": "ID", "filedKey": "product_id", "mappedTo": "entity_id", "type": "string", "disabled": True},
            {"name": "Title", "filedKey": "title", "mappedTo": "name", "type": "string", "disabled": True},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": True},
            {"name": "Vendor", "filedKey": "vendor", "mappedTo": "vendor", "type": "string", "disabled": False},
            {
                "name": "Product Type",
                "filedKey": "product_type",
                "mappedTo": "product_type",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Description",
                "filedKey": "description",
                "mappedTo": "plainTextDescription",
                "type": "string",
                "disabled": False,
            },
            {"name": "Title", "filedKey": "title", "mappedTo": "title", "type": "string", "disabled": False},
            {"name": "Tags", "filedKey": "tags", "mappedTo": "tags", "type": "string", "disabled": False},
        ],
        "variant": [
            {"name": "ID", "filedKey": "variant_id", "mappedTo": "entity_id", "type": "string", "disabled": True},
            {
                "name": "Image URL",
                "filedKey": "image_url",
                "mappedTo": "default_image",
                "type": "string",
                "disabled": True,
            },
            {
                "name": "Display Name",
                "filedKey": "display_name",
                "mappedTo": "name",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Description",
                "filedKey": "description",
                "mappedTo": "plainTextDescription",
                "type": "string",
                "disabled": False,
            },
            {"name": "Tags", "filedKey": "tags", "mappedTo": "tags", "type": "string", "disabled": False},
            {"name": "Price", "filedKey": "price", "mappedTo": "price", "type": "string", "disabled": False},
            {
                "name": "Compare At Price",
                "filedKey": "compare_at_price",
                "mappedTo": "compare_at_price",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Inventory Quantity",
                "filedKey": "inventory_quantity",
                "mappedTo": "inventory",
                "type": "string",
                "disabled": False,
            },
            {"name": "URL", "filedKey": "url", "mappedTo": "online_store_url", "type": "string", "disabled": False},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": False},
        ],
    }
}
