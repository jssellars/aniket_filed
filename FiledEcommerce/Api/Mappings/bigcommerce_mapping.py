bigcommerce_mapping = {
    "mapping": {
        "product": [
            {"name": "ID", "filedKey": "product_id", "mappedTo": "entity_id", "type": "string", "disabled": True},
            {"name": "Title", "filedKey": "title", "mappedTo": "name", "type": "string", "disabled": True},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": True},
            {
                "name": "Product Type",
                "filedKey": "product_type",
                "mappedTo": "type",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Description",
                "filedKey": "description",
                "mappedTo": "plain_text_description",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Image URL",
                "filedKey": "image_url",
                "mappedTo": "default_image",
                "type": "string",
                "disabled": True,
            },
            {"name": "Tags", "filedKey": "tags", "mappedTo": "categories", "type": "string", "disabled": False},
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
                "mappedTo": "plain_text_description",
                "type": "string",
                "disabled": False,
            },
            {"name": "Tags", "filedKey": "tags", "mappedTo": "categories", "type": "string", "disabled": False},
            {"name": "Price", "filedKey": "price", "mappedTo": "sale_price", "type": "string", "disabled": False},
            {
                "name": "Compare At Price",
                "filedKey": "compare_at_price",
                "mappedTo": "base_price",
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
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": False},
        ],
    }
}
