from facebook_business.adobjects.productcatalog import ProductCatalog as FacebookProductCatalog
from facebook_business.adobjects.productgroup import ProductGroup as FacebookProductGroup
from facebook_business.adobjects.productitem import ProductItem as FacebookProductItem
from facebook_business.adobjects.productset import ProductSet as FacebookProductSet

PRODUCT_SETS_FIELD_BY_PRODUCT = 'product_sets'

PRODUCT_CATALOGS_FIELDS = [FacebookProductCatalog.Field.name,
                           FacebookProductCatalog.Field.vertical,
                           FacebookProductCatalog.Field.id,
                           FacebookProductCatalog.Field.business,
                           FacebookProductCatalog.Field.da_display_settings,
                           FacebookProductCatalog.Field.default_image_url,
                           FacebookProductCatalog.Field.fallback_image_url,
                           FacebookProductCatalog.Field.feed_count,
                           FacebookProductCatalog.Field.is_catalog_segment,
                           FacebookProductCatalog.Field.product_count,
                           FacebookProductCatalog.Field.store_catalog_settings]

PRODUCT_SETS_FIELDS = [FacebookProductSet.Field.auto_creation_url,
                       FacebookProductSet.Field.filter,
                       FacebookProductSet.Field.id,
                       FacebookProductSet.Field.name,
                       FacebookProductSet.Field.product_count,
                       FacebookProductSet.Field.product_catalog]

PRODUCT_GROUPS_FIELDS = [FacebookProductGroup.Field.id,
                         FacebookProductGroup.Field.product_catalog,
                         FacebookProductGroup.Field.retailer_id,
                         FacebookProductGroup.Field.variants]

PRODUCT_FIELDS = [FacebookProductItem.Field.id,
                  FacebookProductItem.Field.currency,
                  FacebookProductItem.Field.description,
                  FacebookProductItem.Field.url,
                  FacebookProductItem.Field.availability,
                  FacebookProductItem.Field.name,
                  FacebookProductItem.Field.price,
                  FacebookProductItem.Field.product_group,
                  FacebookProductItem.Field.category,
                  FacebookProductItem.Field.product_type,
                  FacebookProductItem.Field.short_description,
                  FacebookProductItem.Field.custom_data,
                  FacebookProductItem.Field.custom_label_0,
                  FacebookProductItem.Field.custom_label_1,
                  FacebookProductItem.Field.custom_label_2,
                  FacebookProductItem.Field.custom_label_3,
                  FacebookProductItem.Field.custom_label_4,
                  FacebookProductItem.Field.additional_image_urls,
                  FacebookProductItem.Field.additional_variant_attributes,
                  FacebookProductItem.Field.age_group,
                  FacebookProductItem.Field.image_url,
                  FacebookProductItem.Field.image_cdn_urls,
                  FacebookProductItem.Field.gender,
                  FacebookProductItem.Field.brand,
                  FacebookProductItem.Field.color,
                  FacebookProductItem.Field.condition,
                  FacebookProductItem.Field.expiration_date,
                  FacebookProductItem.Field.inventory,
                  FacebookProductItem.Field.material,
                  FacebookProductItem.Field.pattern,
                  FacebookProductItem.Field.retailer_product_group_id,
                  FacebookProductItem.Field.review_status,
                  FacebookProductItem.Field.review_rejection_reasons,
                  FacebookProductItem.Field.sale_price,
                  FacebookProductItem.Field.sale_price_end_date,
                  FacebookProductItem.Field.sale_price_start_date,
                  FacebookProductItem.Field.shipping_weight_unit,
                  FacebookProductItem.Field.shipping_weight_value,
                  FacebookProductItem.Field.size,
                  FacebookProductItem.Field.offer_price_amount,
                  FacebookProductItem.Field.offer_price_end_date,
                  FacebookProductItem.Field.offer_price_start_date,
                  PRODUCT_SETS_FIELD_BY_PRODUCT]
