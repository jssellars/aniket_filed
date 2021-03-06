woocommerce_mapping = {
    "mapping": {
        "product": [{
            "name": "ID",
            "filedKey": "product_id",
            "mappedTo": "id",
            "type": "string",
            "disabled": False,
        },
            {
                "name": "Title",
                "filedKey": "title",
                "mappedTo": "name",
                "type": "string",
                "disabled": False,
            },
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
                "mappedTo": "description",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Title",
                "filedKey": "title",
                "mappedTo": "name",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "tags",
                "filedKey": "tags",
                "mappedTo": "tags",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "SKU",
                "filedKey": "sku",
                "mappedTo": "sku",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Image URL",
                "filedKey": "image_url",
                "mappedTo": "images",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Availability",
                "filedKey": "availability",
                "mappedTo": "purchasable",
                "type": "string",
                "disabled": False,
            }
        ],
        "variant": [{
            "name": "ID",
            "filedKey": "variant_id",
            "mappedTo": "id",
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
            {
                "name": "sale_price",
                "filedKey": "price",
                "mappedTo": "price",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Image URL",
                "filedKey": "image_url",
                "mappedTo": "image",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Price",
                "filedKey": "compare_at_price",
                "mappedTo": "price",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "on_sale",
                "filedKey": "availability",
                "mappedTo": "availability",
                "type": "boolean",
                "disabled": False,
            },
            {
                "name": "stock_quantity",
                "filedKey": "inventory_quantity",
                "mappedTo": "inventory_quantity",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "permalink",
                "filedKey": "url",
                "mappedTo": "url",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "Availability",
                "filedKey": "availability",
                "mappedTo": "stock_status",
                "type": "string",
                "disabled": False,
            },
            {
                "name": "SKU",
                "filedKey": "sku",
                "mappedTo": "sku",
                "type": "string",
                "disabled": False,
            }
        ]
    }
}
