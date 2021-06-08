shopify_mapping = {
    "mapping": {
        "product": [
            {"name": "ID", "filedKey": "product_id", "mappedTo": "id", "type": "string", "disabled": True},
            {"name": "Title", "filedKey": "title", "mappedTo": "title", "type": "string", "disabled": True},
            {
                "name": "Image URL",
                "filedKey": "image_url",
                "mappedTo": "featured_image",
                "type": "string",
                "disabled": True,
            },
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
                "mappedTo": "description",
                "type": "string",
                "disabled": False,
            },
            {"name": "Title", "filedKey": "title", "mappedTo": "title", "type": "string", "disabled": False},
            {"name": "Tags", "filedKey": "tags", "mappedTo": "tags", "type": "string", "disabled": False},
            {"name": "CreatedAt", "filedKey": "created_at", "mappedTo": "created_at", "type": "string", "disabled": False},
            {"name": "UpdatedAt", "filedKey": "updated_at", "mappedTo": "updated_at", "type": "string", "disabled": False},
        ],
        "variant": [
            {"name": "ID", "filedKey": "variant_id", "mappedTo": "id", "type": "string", "disabled": True},
            {"name": "Image URL", "filedKey": "image_url", "mappedTo": "image", "type": "string", "disabled": True},
            {
                "name": "Display Name",
                "filedKey": "display_name",
                "mappedTo": "display_name",
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
                "name": "Availability",
                "filedKey": "availability",
                "mappedTo": "available_for_sale",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Inventory Quantity",
                "filedKey": "inventory_quantity",
                "mappedTo": "inventory_quantity",
                "type": "string",
                "disabled": False,
            },
            {"name": "URL", "filedKey": "url", "mappedTo": "online_store_url", "type": "string", "disabled": False},
            {"name": "SKU", "filedKey": "sku", "mappedTo": "sku", "type": "string", "disabled": False},
            {"name": "Barcode", "filedKey": "barcode", "mappedTo": "barcode", "type": "string", "disabled": False},
        ],
    }
}