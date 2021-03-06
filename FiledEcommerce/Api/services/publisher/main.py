import json

from FiledEcommerce.Api.Models.filed_model import FiledCustomProperties
from FiledEcommerce.Api.utils.models.filed_model import FiledProduct, FiledVariant
from FiledEcommerce.Api.utils.tools.date_utils import get_utc_aware_date
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import *


def publisher_lambda(user_id, filed_product_catalog_id, platform, products):
    products_response = products["products"]

    with engine.connect() as conn:
        ep = external_platforms.alias("ep")
        ep_cols = ep.c
        query = (
            select([ep_cols.Id, ep_cols.CreatedByFirstName, ep_cols.CreatedByLastName])
            .select_from(ep.join(platforms, ep_cols.PlatformId == pl.Id, isouter=True))
            .where(pl.Value == platform)
            .where(ext_plat_cols.CreatedById == user_id)
            .limit(1)
        )
        for row in conn.execute(query):
            row_li = list(row)
        external_platform_id, user_first_name, user_last_name = row_li

        # ALL MAPPED PRODUCTS SHOULD BE ACTIVE BY DEFAULT
        default_state = 1
        filed_set_ins = filed_sets.insert().values(
            UpdatedAt=get_utc_aware_date(),
            UpdatedById=user_id,
            UpdatedByFirstName=user_first_name,
            UpdatedByLastName=user_last_name,
            CreatedAt=get_utc_aware_date(),
            CreatedById=user_id,
            CreatedByFirstName=user_first_name,
            CreatedByLastName=user_last_name,
            FiledProductCatalogId=filed_product_catalog_id[0],
            Name=f"{platform} Products Set",
            StateId=1,
            ImportedAt=get_utc_aware_date(),
        )
        fs_results = conn.execute(filed_set_ins)
        filed_set_id = fs_results.inserted_primary_key

        for product in products_response:
            product = FiledProduct(**product)

            fp_ins = filed_products.insert().values(
                UpdatedAt=product.updated_at,
                CreatedAt=product.created_at,
                ImportedAt=product.imported_at,
                CreatedById=user_id,
                CreatedByFirstName=user_first_name,
                CreatedByLastName=user_last_name,
                ImageUrl=product.image_url,
                Name=product.title,
                ProductType=product.product_type,
                Description=product.description,
                Sku=product.sku or 0,
                # TODO: Add Vendor to FiledProducts Table, otherwise this insert should stay commented out
                # Vendor=product.vendor,
                Tags=product.tags,
                Availability=product.availability,
                Brand=product.brand,
                StateId=default_state,
                FiledProductCatalogId=filed_product_catalog_id[0],
            )
            result = conn.execute(fp_ins)
            filed_product_id = result.inserted_primary_key

            fp_conn_ins = filed_product_conns.insert().values(
                IdInPlatform=product.product_id,
                ExternalPlatformId=external_platform_id,
                FiledProductId=filed_product_id[0],
            )
            conn.execute(fp_conn_ins)

            for variant in product.variants:
                variant = FiledVariant(**variant)
                variant.filed_product_id = filed_product_id[0]

                fv_ins = filed_variants.insert().values(
                    UpdatedAt=variant.updated_at,
                    CreatedAt=variant.created_at,
                    ImportedAt=variant.imported_at,
                    CreatedByFirstName=user_first_name,
                    CreatedByLastName=user_last_name,
                    CreatedById=user_id,
                    ImageUrl=variant.image_url,
                    Name=variant.display_name,
                    FiledProductId=variant.filed_product_id,
                    ShortDescription=variant.description[:128],
                    Description=variant.description,
                    InventoryQuantity=variant.inventory_quantity or 0,
                    Sku=variant.sku or 0,
                    Url=variant.url,
                    Barcode=variant.barcode,
                    Price=variant.price or 0,
                    CompareAtPrice=variant.compare_at_price or 0,
                    Availability=variant.availability,
                    Tags=variant.tags,
                    Material=variant.material,
                    Condition=variant.condition,
                    Color=variant.color,
                    Size=variant.size,
                    CurrencyId=variant.currency_id,
                    StateId=default_state,
                    FiledProductCatalogId=filed_product_catalog_id[0],
                )
                fv_result = conn.execute(fv_ins)

                filed_variant_id = fv_result.inserted_primary_key

                fv_conn_ins = filed_variant_conns.insert().values(
                    IdInPlatform=variant.variant_id,
                    ExternalPlatformId=external_platform_id,
                    FiledVariantId=filed_variant_id[0],
                )
                conn.execute(fv_conn_ins)

                if isinstance(variant.custom_props, dict):
                    custom_props = variant.custom_props["properties"]
                elif isinstance(variant.custom_props, FiledCustomProperties):
                    custom_props = variant.custom_props.properties
                else:
                    custom_props = None
                custom_properties_ins = custom_properties.insert().values(
                    FiledVariantId=filed_variant_id, Properties=json.dumps(custom_props)
                )
                conn.execute(custom_properties_ins)

                filed_sets_variants_ins = filed_set_variants.insert().values(
                    FiledVariantId=filed_variant_id[0],
                    FiledSetId=filed_set_id[0],
                )
                conn.execute(filed_sets_variants_ins)

    return {"filedSetId": filed_set_id[0]}
