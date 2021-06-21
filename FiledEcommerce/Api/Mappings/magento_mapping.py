magento_mapping = {
    "mapping": {
        "product": [
            {"name": "ID", "filedKey": "product_id", "mappedTo": "id", "type": "string", "disabled": True},
            {"name": "Title", "filedKey": "title", "mappedTo": "name", "type": "string", "disabled": True},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "name", "sku": "string", "disabled": True},
            {
                "name": "Image URL",
                "filedKey": "image_url",
                "mappedTo": "image",
                "type": "string",
                "disabled": True,
            },
            {
                "name": "Product Type",
                "filedKey": "product_type",
                "mappedTo": "categories",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Description",
                "filedKey": "description",
                "mappedTo": "description",
                "type": "string",
                "disabled": False,
            },
            {"name": "Tags", "filedKey": "tags", "mappedTo": "meta_keyword", "type": "string", "disabled": False},
            {"name": "Title", "filedKey": "title", "mappedTo": "name", "type": "string", "disabled": False},
        ],
        "variant": [
            {"name": "ID", "filedKey": "variant_id", "mappedTo": "id", "type": "string", "disabled": True},
            {"name": "Image URL", "filedKey": "image_url", "mappedTo": "image", "type": "string", "disabled": True},
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
                "mappedTo": "description",
                "type": "string",
                "disabled": False,
            },
            {"name": "Tags", "filedKey": "tags", "mappedTo": "meta_keyword", "type": "string", "disabled": False},
            {"name": "Price", "filedKey": "price", "mappedTo": "price", "type": "string", "disabled": False},
            {
                "name": "Availability",
                "filedKey": "availability",
                "mappedTo": "stock_status",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Inventory Quantity",
                "filedKey": "inventory_quantity",
                "mappedTo": "only_x_left_in_stock",
                "type": "string",
                "disabled": False,
            },
            {"name": "URL", "filedKey": "url", "mappedTo": "canonical_url", "type": "string", "disabled": False},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": False},
        ],
    }
}