from sgqlc import types
from sgqlc.types import datetime, relay

shopify_schema = types.Schema()

# Unexport Node/PageInfo, let schema re-declare them
shopify_schema -= relay.Node
shopify_schema -= relay.PageInfo

########################################################################
# Scalars and Enumerations
########################################################################
Boolean = types.Boolean
Int = types.Int
Float = types.Float
String = types.String
ID = types.ID
Date = datetime.Date
DateTime = datetime.DateTime
Field = types.Field
Arg = types.Arg


class CollectionRuleColumn(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('TAG', 'TITLE', 'TYPE', 'VENDOR', 'VARIANT_PRICE', 'IS_PRICE_REDUCED', 'VARIANT_COMPARE_AT_PRICE', 'VARIANT_WEIGHT', 'VARIANT_INVENTORY', 'VARIANT_TITLE')


class CollectionRuleRelation(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('CONTAINS', 'ENDS_WITH', 'EQUALS', 'GREATER_THAN', 'IS_NOT_SET', 'IS_SET', 'LESS_THAN', 'NOT_CONTAINS', 'NOT_EQUALS', 'STARTS_WITH')


class CollectionSortKeys(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('TITLE', 'UPDATED_AT', 'ID', 'RELEVANCE')


class CollectionSortOrder(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('ALPHA_ASC', 'ALPHA_DESC', 'BEST_SELLING', 'CREATED', 'CREATED_DESC', 'MANUAL', 'PRICE_ASC', 'PRICE_DESC')


class CropRegion(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('CENTER', 'TOP', 'BOTTOM', 'LEFT', 'RIGHT')


class CurrencyCode(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('USD', 'EUR', 'GBP', 'CAD', 'AFN', 'ALL', 'DZD', 'AOA', 'ARS', 'AMD', 'AWG', 'AUD', 'BBD', 'AZN', 'BDT', 'BSD', 'BHD', 'BIF', 'BZD', 'BMD', 'BTN', 'BAM', 'BRL', 'BOB', 'BWP', 'BND', 'BGN', 'MMK', 'KHR', 'CVE', 'KYD', 'XAF', 'CLP', 'CNY', 'COP', 'KMF', 'CDF', 'CRC', 'HRK', 'CZK', 'DKK', 'DJF', 'DOP', 'XCD', 'EGP', 'ERN', 'ETB', 'FKP', 'XPF', 'FJD', 'GIP', 'GMD', 'GHS', 'GTQ', 'GYD', 'GEL', 'GNF', 'HTG', 'HNL', 'HKD', 'HUF', 'ISK', 'INR', 'IDR', 'ILS', 'IRR', 'IQD', 'JMD', 'JPY', 'JEP', 'JOD', 'KZT', 'KES', 'KID', 'KWD', 'KGS', 'LAK', 'LVL', 'LBP', 'LSL', 'LRD', 'LYD', 'LTL', 'MGA', 'MKD', 'MOP', 'MWK', 'MVR', 'MRU', 'MXN', 'MYR', 'MUR', 'MDL', 'MAD', 'MNT', 'MZN', 'NAD', 'NPR', 'ANG', 'NZD', 'NIO', 'NGN', 'NOK', 'OMR', 'PAB', 'PKR', 'PGK', 'PYG', 'PEN', 'PHP', 'PLN', 'QAR', 'RON', 'RUB', 'RWF', 'WST', 'SHP', 'SAR', 'STD', 'RSD', 'SCR', 'SLL', 'SGD', 'SDG', 'SOS', 'SYP', 'ZAR', 'KRW', 'SSP', 'SBD', 'LKR', 'SRD', 'SZL', 'SEK', 'CHF', 'TWD', 'THB', 'TJS', 'TZS', 'TOP', 'TTD', 'TND', 'TRY', 'TMT', 'UGX', 'UAH', 'AED', 'UYU', 'UZS', 'VUV', 'VES', 'VND', 'XOF', 'YER', 'ZMW')


class Decimal(types.Scalar):
    __schema__ = shopify_schema


class HTML(types.Scalar):
    __schema__ = shopify_schema


class ImageContentType(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('PNG', 'JPG', 'WEBP')


class MediaContentType(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('VIDEO', 'EXTERNAL_VIDEO', 'MODEL_3D', 'IMAGE')


class MediaErrorCode(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('UNKNOWN', 'INVALID_SIGNED_URL', 'IMAGE_DOWNLOAD_FAILURE', 'IMAGE_PROCESSING_FAILURE', 'MEDIA_TIMEOUT_ERROR', 'EXTERNAL_VIDEO_NOT_FOUND', 'EXTERNAL_VIDEO_UNLISTED', 'EXTERNAL_VIDEO_INVALID_ASPECT_RATIO', 'VIDEO_METADATA_READ_ERROR', 'VIDEO_INVALID_FILETYPE_ERROR', 'VIDEO_MIN_WIDTH_ERROR', 'VIDEO_MAX_WIDTH_ERROR', 'VIDEO_MIN_HEIGHT_ERROR', 'VIDEO_MAX_HEIGHT_ERROR', 'VIDEO_MIN_DURATION_ERROR', 'VIDEO_MAX_DURATION_ERROR', 'VIDEO_VALIDATION_ERROR', 'MODEL3D_VALIDATION_ERROR', 'MODEL3D_THUMBNAIL_GENERATION_ERROR', 'MODEL3D_GLB_TO_USDZ_CONVERSION_ERROR', 'MODEL3D_GLB_OUTPUT_CREATION_ERROR', 'UNSUPPORTED_IMAGE_FILE_TYPE', 'INVALID_IMAGE_FILE_SIZE')


class MediaPreviewImageStatus(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('UPLOADED', 'PROCESSING', 'READY', 'FAILED')


class MediaStatus(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('UPLOADED', 'PROCESSING', 'READY', 'FAILED')


class MediaUserErrorCode(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('INVALID', 'BLANK', 'VIDEO_VALIDATION_ERROR', 'MODEL3D_VALIDATION_ERROR', 'VIDEO_THROTTLE_EXCEEDED', 'MODEL3D_THROTTLE_EXCEEDED', 'PRODUCT_MEDIA_LIMIT_EXCEEDED', 'SHOP_MEDIA_LIMIT_EXCEEDED', 'PRODUCT_DOES_NOT_EXIST', 'MEDIA_DOES_NOT_EXIST', 'MEDIA_DOES_NOT_EXIST_ON_PRODUCT', 'TOO_MANY_MEDIA_PER_INPUT_PAIR', 'MAXIMUM_VARIANT_MEDIA_PAIRS_EXCEEDED', 'INVALID_MEDIA_TYPE', 'PRODUCT_VARIANT_SPECIFIED_MULTIPLE_TIMES', 'PRODUCT_VARIANT_DOES_NOT_EXIST_ON_PRODUCT', 'NON_READY_MEDIA', 'PRODUCT_VARIANT_ALREADY_HAS_MEDIA', 'MEDIA_IS_NOT_ATTACHED_TO_VARIANT', 'MEDIA_CANNOT_BE_MODIFIED')


class MetafieldOwnerType(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('ARTICLE', 'BLOG', 'COLLECTION', 'CUSTOMER', 'DRAFTORDER', 'ORDER', 'PAGE', 'PRODUCT', 'PRODUCTIMAGE', 'PRODUCTVARIANT', 'SHOP')


class MetafieldValueType(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('STRING', 'INTEGER', 'JSON_STRING')


class Money(types.Scalar):
    __schema__ = shopify_schema


class PrivateMetafieldValueType(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('STRING', 'INTEGER', 'JSON_STRING')


class ProductCollectionSortKeys(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('TITLE', 'PRICE', 'BEST_SELLING', 'CREATED', 'ID', 'MANUAL', 'COLLECTION_DEFAULT', 'RELEVANCE')


class ProductImageSortKeys(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('CREATED_AT', 'POSITION', 'ID', 'RELEVANCE')


class ProductMediaSortKeys(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('POSITION', 'ID', 'RELEVANCE')


class ProductSortKeys(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('TITLE', 'PRODUCT_TYPE', 'VENDOR', 'INVENTORY_TOTAL', 'UPDATED_AT', 'CREATED_AT', 'PUBLISHED_AT', 'ID', 'RELEVANCE')


class ProductStatus(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('ACTIVE', 'ARCHIVED', 'DRAFT')


class ProductVariantSortKeys(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('TITLE', 'NAME', 'SKU', 'INVENTORY_QUANTITY', 'INVENTORY_MANAGEMENT', 'INVENTORY_LEVELS_AVAILABLE', 'INVENTORY_POLICY', 'FULL_TITLE', 'POPULAR', 'POSITION', 'ID', 'RELEVANCE')


class UnsignedInt64(types.Scalar):
    __schema__ = shopify_schema


class URL(types.Scalar):
    __schema__ = shopify_schema


class StorefrontID(types.Scalar):
    __schema__ = shopify_schema


class WeightUnit(types.Enum):
    __schema__ = shopify_schema
    __choices__ = ('KILOGRAMS', 'GRAMS', 'POUNDS', 'OUNCES')


########################################################################
# Basic Interfaces and Types
########################################################################
class HasMetafields(types.Interface):
    __schema__ = shopify_schema
    __field_names__ = ('metafield', 'metafields', 'private_metafield', 'private_metafields')
    metafield = types.Field('Metafield', graphql_name='metafield', args=types.ArgDict((
        ('namespace', types.Arg(types.non_null(String), graphql_name='namespace', default=None)),
        ('key', types.Arg(types.non_null(String), graphql_name='key', default=None)),
))
    )
    metafields = types.Field(types.non_null('MetafieldConnection'), graphql_name='metafields', args=types.ArgDict((
        ('namespace', types.Arg(String, graphql_name='namespace', default=None)),
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
))
    )
    private_metafield = types.Field('PrivateMetafield', graphql_name='privateMetafield', args=types.ArgDict((
        ('namespace', types.Arg(types.non_null(String), graphql_name='namespace', default=None)),
        ('key', types.Arg(types.non_null(String), graphql_name='key', default=None)),
))
    )
    private_metafields = types.Field(types.non_null('PrivateMetafieldConnection'), graphql_name='privateMetafields', args=types.ArgDict((
        ('namespace', types.Arg(String, graphql_name='namespace', default=None)),
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
))
    )


class LegacyInteroperability(types.Interface):
    __schema__ = shopify_schema
    __field_names__ = ('legacy_resource_id',)
    legacy_resource_id = types.Field(types.non_null(UnsignedInt64), graphql_name='legacyResourceId')


class Navigable(types.Interface):
    __schema__ = shopify_schema
    __field_names__ = ('default_cursor',)
    default_cursor = types.Field(types.non_null(String), graphql_name='defaultCursor')


class Node(types.Interface):
    __schema__ = shopify_schema
    __field_names__ = ('id',)
    id = types.Field(types.non_null(ID), graphql_name='id')


class OnlineStorePreviewable(types.Interface):
    __schema__ = shopify_schema
    __field_names__ = ('online_store_preview_url',)
    online_store_preview_url = types.Field(URL, graphql_name='onlineStorePreviewUrl')


class PageInfo(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('has_next_page', 'has_previous_page')
    has_next_page = types.Field(types.non_null(Boolean), graphql_name='hasNextPage')
    has_previous_page = types.Field(types.non_null(Boolean), graphql_name='hasPreviousPage')


class MoneyV2(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('amount', 'currency_code')
    amount = types.Field(types.non_null(Decimal), graphql_name='amount')
    currency_code = types.Field(types.non_null(CurrencyCode), graphql_name='currencyCode')


class SelectedOption(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('name', 'value')
    name = types.Field(types.non_null(String), graphql_name='name')
    value = types.Field(types.non_null(String), graphql_name='value')


class SEO(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('description', 'title')
    description = types.Field(String, graphql_name='description')
    title = types.Field(String, graphql_name='title')


########################################################################
# Objects and Edges and Connections
########################################################################

# ################## Image ##################
class Image(types.Type, HasMetafields):
    __schema__ = shopify_schema
    __field_names__ = ('alt_text', 'id', 'original_src', 'transformed_src')
    alt_text = types.Field(String, graphql_name='altText')
    id = types.Field(ID, graphql_name='id')
    original_src = types.Field(types.non_null(URL), graphql_name='originalSrc')
    transformed_src = types.Field(types.non_null(URL), graphql_name='transformedSrc', args=types.ArgDict((
        ('max_width', types.Arg(Int, graphql_name='maxWidth', default=None)),
        ('max_height', types.Arg(Int, graphql_name='maxHeight', default=None)),
        ('crop', types.Arg(CropRegion, graphql_name='crop', default=None)),
        ('scale', types.Arg(Int, graphql_name='scale', default=1)),
        ('preferred_content_type', types.Arg(ImageContentType, graphql_name='preferredContentType', default=None)),))
    )


class ImageConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('ImageEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null('PageInfo'), graphql_name='pageInfo')


class ImageEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('Image'), graphql_name='node')


# ################## Media ##################
class Media(types.Interface):
    __schema__ = shopify_schema
    __field_names__ = ('alt', 'media_content_type', 'media_errors', 'preview', 'status')
    alt = types.Field(String, graphql_name='alt')
    media_content_type = types.Field(types.non_null(MediaContentType), graphql_name='mediaContentType')
    media_errors = types.Field(types.non_null(types.list_of(types.non_null('MediaError'))), graphql_name='mediaErrors')
    preview = types.Field('MediaPreviewImage', graphql_name='preview')
    status = types.Field(types.non_null(MediaStatus), graphql_name='status')


class MediaError(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('code', 'details', 'message')
    code = types.Field(types.non_null(MediaErrorCode), graphql_name='code')
    details = types.Field(String, graphql_name='details')
    message = types.Field(types.non_null(String), graphql_name='message')


class MediaPreviewImage(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('image', 'status')
    image = types.Field('Image', graphql_name='image')
    status = types.Field(types.non_null(MediaPreviewImageStatus), graphql_name='status')


class MediaConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('MediaEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null('PageInfo'), graphql_name='pageInfo')


class MediaEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('Media'), graphql_name='node')


# ################## Metafield ##################
class Metafield(types.Type, Node, LegacyInteroperability):
    __schema__ = shopify_schema
    __field_names__ = ('created_at', 'description', 'key', 'namespace', 'owner_type', 'updated_at', 'value', 'value_type')
    created_at = types.Field(types.non_null(DateTime), graphql_name='createdAt')
    description = types.Field(String, graphql_name='description')
    key = types.Field(types.non_null(String), graphql_name='key')
    namespace = types.Field(types.non_null(String), graphql_name='namespace')
    owner_type = types.Field(types.non_null(MetafieldOwnerType), graphql_name='ownerType')
    updated_at = types.Field(types.non_null(DateTime), graphql_name='updatedAt')
    value = types.Field(types.non_null(String), graphql_name='value')
    value_type = types.Field(types.non_null(MetafieldValueType), graphql_name='valueType')


class MetafieldConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('MetafieldEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null('PageInfo'), graphql_name='pageInfo')


class MetafieldEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('Metafield'), graphql_name='node')


class PrivateMetafield(types.Type, Node):
    __schema__ = shopify_schema
    __field_names__ = ('created_at', 'key', 'namespace', 'updated_at', 'value', 'value_type')
    created_at = types.Field(types.non_null(DateTime), graphql_name='createdAt')
    key = types.Field(types.non_null(String), graphql_name='key')
    namespace = types.Field(types.non_null(String), graphql_name='namespace')
    updated_at = types.Field(types.non_null(DateTime), graphql_name='updatedAt')
    value = types.Field(types.non_null(String), graphql_name='value')
    value_type = types.Field(types.non_null(PrivateMetafieldValueType), graphql_name='valueType')


class PrivateMetafieldConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('PrivateMetafieldEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null(PageInfo), graphql_name='pageInfo')


class PrivateMetafieldEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('PrivateMetafield'), graphql_name='node')


########################################################################
# Collection and Product => Edges and Connections
########################################################################
class CollectionConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('CollectionEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null('PageInfo'), graphql_name='pageInfo')


class CollectionEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('Collection'), graphql_name='node')


class ProductConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('ProductEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null(PageInfo), graphql_name='pageInfo')


class ProductEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('Product'), graphql_name='node')


class ProductVariantConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('ProductVariantEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null(PageInfo), graphql_name='pageInfo')


class ProductVariantEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('ProductVariant'), graphql_name='node')


class ProductVariantPricePairConnection(relay.Connection):
    __schema__ = shopify_schema
    __field_names__ = ('edges', 'page_info')
    edges = types.Field(types.non_null(types.list_of(types.non_null('ProductVariantPricePairEdge'))), graphql_name='edges')
    page_info = types.Field(types.non_null(PageInfo), graphql_name='pageInfo')


class ProductVariantPricePairEdge(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('cursor', 'node')
    cursor = types.Field(types.non_null(String), graphql_name='cursor')
    node = types.Field(types.non_null('ProductVariantPricePair'), graphql_name='node')


########################################################################
# Collection and Product => Objects
########################################################################

# ################## Product ##################
class ProductVariantPricePair(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('compare_at_price', 'price')
    compare_at_price = types.Field(MoneyV2, graphql_name='compareAtPrice')
    price = types.Field(types.non_null(MoneyV2), graphql_name='price')


class ProductPriceRangeV2(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('max_variant_price', 'min_variant_price')
    max_variant_price = types.Field(types.non_null(MoneyV2), graphql_name='maxVariantPrice')
    min_variant_price = types.Field(types.non_null(MoneyV2), graphql_name='minVariantPrice')


class ProductOption(types.Type, Node):
    __schema__ = shopify_schema
    __field_names__ = ('name', 'position', 'values')
    name = types.Field(types.non_null(String), graphql_name='name')
    position = types.Field(types.non_null(Int), graphql_name='position')
    values = types.Field(types.non_null(types.list_of(types.non_null(String))), graphql_name='values')


class Product(types.Type, Node, Navigable, HasMetafields, OnlineStorePreviewable, LegacyInteroperability):
    __schema__ = shopify_schema
    __field_names__ = (
        'collections',
        'created_at',
        'description',
        'description_html',
        'featured_image',
        'featured_media',
        'handle',
        'has_only_default_variant',
        'has_out_of_stock_variants',
        'images',
        'in_collection',
        'is_gift_card',
        'media',
        'media_count',
        'online_store_url',
        'options',
        'price_range_v2',
        'product_type',
        'published_at',
        'seo',
        'status',
        'storefront_id',
        'tags',
        'template_suffix',
        'title',
        'total_inventory',
        'total_variants',
        'tracks_inventory',
        'updated_at',
        'variants',
        'vendor'
    )
    collections = types.Field(types.non_null(CollectionConnection), graphql_name='collections', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(CollectionSortKeys, graphql_name='sortKey', default='ID')),
        ('query', types.Arg(String, graphql_name='query', default=None)),
    )))
    created_at = types.Field(types.non_null(DateTime), graphql_name='createdAt')
    description = types.Field(types.non_null(String), graphql_name='description', args=types.ArgDict((
        ('truncate_at', types.Arg(Int, graphql_name='truncateAt', default=None)),
    )))
    description_html = types.Field(types.non_null(HTML), graphql_name='descriptionHtml')
    featured_image = types.Field(Image, graphql_name='featuredImage')
    featured_media = types.Field(Media, graphql_name='featuredMedia')
    handle = types.Field(types.non_null(String), graphql_name='handle')
    has_only_default_variant = types.Field(types.non_null(Boolean), graphql_name='hasOnlyDefaultVariant')
    has_out_of_stock_variants = types.Field(types.non_null(Boolean), graphql_name='hasOutOfStockVariants')
    images = types.Field(types.non_null(ImageConnection), graphql_name='images', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(ProductImageSortKeys, graphql_name='sortKey', default='POSITION')),
        ('max_width', types.Arg(Int, graphql_name='maxWidth', default=None)),
        ('max_height', types.Arg(Int, graphql_name='maxHeight', default=None)),
        ('crop', types.Arg(CropRegion, graphql_name='crop', default=None)),
        ('scale', types.Arg(Int, graphql_name='scale', default=1)),
    )))
    in_collection = types.Field(types.non_null(Boolean), graphql_name='inCollection', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    is_gift_card = types.Field(types.non_null(Boolean), graphql_name='isGiftCard')
    media = types.Field(types.non_null(MediaConnection), graphql_name='media', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(ProductMediaSortKeys, graphql_name='sortKey', default='POSITION')),
    )))
    media_count = types.Field(types.non_null(Int), graphql_name='mediaCount')
    online_store_url = types.Field(URL, graphql_name='onlineStoreUrl')
    options = types.Field(types.non_null(types.list_of(types.non_null('ProductOption'))), graphql_name='options', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
    )))
    price_range_v2 = types.Field(types.non_null(ProductPriceRangeV2), graphql_name='priceRangeV2')
    product_type = types.Field(types.non_null(String), graphql_name='productType')
    published_at = types.Field(DateTime, graphql_name='publishedAt')
    seo = types.Field(types.non_null(SEO), graphql_name='seo')
    status = types.Field(types.non_null(ProductStatus), graphql_name='status')
    storefront_id = types.Field(types.non_null(StorefrontID), graphql_name='storefrontId')
    tags = types.Field(types.non_null(types.list_of(types.non_null(String))), graphql_name='tags')
    template_suffix = types.Field(String, graphql_name='templateSuffix')
    title = types.Field(types.non_null(String), graphql_name='title')
    total_inventory = types.Field(types.non_null(Int), graphql_name='totalInventory')
    total_variants = types.Field(types.non_null(Int), graphql_name='totalVariants')
    tracks_inventory = types.Field(types.non_null(Boolean), graphql_name='tracksInventory')
    updated_at = types.Field(types.non_null(DateTime), graphql_name='updatedAt')
    variants = types.Field(types.non_null(ProductVariantConnection), graphql_name='variants', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(ProductVariantSortKeys, graphql_name='sortKey', default='POSITION')),
    )))
    vendor = types.Field(types.non_null(String), graphql_name='vendor')


class ProductVariant(types.Type, Node, HasMetafields, Navigable, LegacyInteroperability):
    __schema__ = shopify_schema
    __field_names__ = (
        'available_for_sale',
        'barcode',
        'compare_at_price',
        'created_at',
        'display_name',
        'image',
        'inventory_quantity',
        'media',
        'position',
        'presentment_prices',
        'price',
        'product',
        'selected_options',
        'sku',
        'storefront_id',
        'tax_code',
        'taxable',
        'title',
        'updated_at',
        'weight',
        'weight_unit'
    )
    available_for_sale = types.Field(types.non_null(Boolean), graphql_name='availableForSale')
    barcode = types.Field(String, graphql_name='barcode')
    compare_at_price = types.Field(Money, graphql_name='compareAtPrice')
    created_at = types.Field(types.non_null(DateTime), graphql_name='createdAt')
    display_name = types.Field(types.non_null(String), graphql_name='displayName')
    image = types.Field(Image, graphql_name='image', args=types.ArgDict((
        ('max_width', types.Arg(Int, graphql_name='maxWidth', default=None)),
        ('max_height', types.Arg(Int, graphql_name='maxHeight', default=None)),
        ('crop', types.Arg(CropRegion, graphql_name='crop', default=None)),
        ('scale', types.Arg(Int, graphql_name='scale', default=1)),
    )))
    inventory_quantity = types.Field(Int, graphql_name='inventoryQuantity')
    media = types.Field(types.non_null(MediaConnection), graphql_name='media', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
    )))
    position = types.Field(types.non_null(Int), graphql_name='position')
    presentment_prices = types.Field(types.non_null(ProductVariantPricePairConnection), graphql_name='presentmentPrices', args=types.ArgDict((
        ('presentment_currencies', types.Arg(types.list_of(types.non_null(CurrencyCode)), graphql_name='presentmentCurrencies', default=None)),
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
    )))
    price = types.Field(types.non_null(Money), graphql_name='price')
    product = types.Field(types.non_null('Product'), graphql_name='product')
    selected_options = types.Field(types.non_null(types.list_of(types.non_null(SelectedOption))), graphql_name='selectedOptions')
    sku = types.Field(String, graphql_name='sku')
    storefront_id = types.Field(types.non_null(StorefrontID), graphql_name='storefrontId')
    tax_code = types.Field(String, graphql_name='taxCode')
    taxable = types.Field(types.non_null(Boolean), graphql_name='taxable')
    title = types.Field(types.non_null(String), graphql_name='title')
    updated_at = types.Field(types.non_null(DateTime), graphql_name='updatedAt')
    weight = types.Field(Float, graphql_name='weight')
    weight_unit = types.Field(types.non_null(WeightUnit), graphql_name='weightUnit')


# ################## Collection ##################
class CollectionRule(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('column', 'condition', 'relation')
    column = types.Field(types.non_null(CollectionRuleColumn), graphql_name='column')
    condition = types.Field(types.non_null(String), graphql_name='condition')
    relation = types.Field(types.non_null(CollectionRuleRelation), graphql_name='relation')


class CollectionRuleConditions(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('allowed_relations', 'default_relation', 'rule_type')
    allowed_relations = types.Field(types.non_null(types.list_of(types.non_null(CollectionRuleRelation))), graphql_name='allowedRelations')
    default_relation = types.Field(types.non_null(CollectionRuleRelation), graphql_name='defaultRelation')
    rule_type = types.Field(types.non_null(CollectionRuleColumn), graphql_name='ruleType')


class CollectionRuleSet(types.Type):
    __schema__ = shopify_schema
    __field_names__ = ('applied_disjunctively', 'rules')
    applied_disjunctively = types.Field(types.non_null(Boolean), graphql_name='appliedDisjunctively')
    rules = types.Field(types.non_null(types.list_of(types.non_null(CollectionRule))), graphql_name='rules')


class Collection(types.Type, HasMetafields, Node):
    __schema__ = shopify_schema
    __field_names__ = (
        'description',
        'description_html',
        'handle',
        'has_product',
        'image',
        'products',
        'products_count',
        'rule_set',
        'seo',
        'sort_order',
        'storefront_id',
        'template_suffix',
        'title',
        'updated_at'
    )
    description = types.Field(types.non_null(String), graphql_name='description', args=types.ArgDict((
        ('truncate_at', types.Arg(Int, graphql_name='truncateAt', default=None)),
    )))
    description_html = types.Field(types.non_null(HTML), graphql_name='descriptionHtml')
    handle = types.Field(types.non_null(String), graphql_name='handle')
    has_product = types.Field(types.non_null(Boolean), graphql_name='hasProduct', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    image = types.Field('Image', graphql_name='image', args=types.ArgDict((
        ('max_width', types.Arg(Int, graphql_name='maxWidth', default=None)),
        ('max_height', types.Arg(Int, graphql_name='maxHeight', default=None)),
        ('crop', types.Arg(CropRegion, graphql_name='crop', default=None)),
        ('scale', types.Arg(Int, graphql_name='scale', default=1)),
    )))
    products = types.Field(types.non_null(ProductConnection), graphql_name='products', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(ProductCollectionSortKeys, graphql_name='sortKey', default='COLLECTION_DEFAULT')),
        ('query', types.Arg(String, graphql_name='query', default=None)),
    )))
    products_count = types.Field(types.non_null(Int), graphql_name='productsCount')
    rule_set = types.Field(CollectionRuleSet, graphql_name='ruleSet')
    seo = types.Field(types.non_null(SEO), graphql_name='seo')
    sort_order = types.Field(types.non_null(CollectionSortOrder), graphql_name='sortOrder')
    storefront_id = types.Field(types.non_null(StorefrontID), graphql_name='storefrontId')
    template_suffix = types.Field(String, graphql_name='templateSuffix')
    title = types.Field(types.non_null(String), graphql_name='title')
    updated_at = types.Field(types.non_null(DateTime), graphql_name='updatedAt')


########################################################################
# Query Root
########################################################################
class QueryRoot(types.Type):
    __schema__ = shopify_schema
    __field_names__ = (
        'collection',
        'collection_rules_conditions',
        'collections',
        'node',
        'nodes',
        'private_metafield',
        'private_metafields',
        'product',
        'product_variant',
        'product_variants',
        'products',
    )

    # Collection queries
    collection = types.Field('Collection', graphql_name='collection', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    collection_rules_conditions = types.Field(types.non_null(types.list_of(types.non_null(CollectionRuleConditions))), graphql_name='collectionRulesConditions')
    collections = types.Field(types.non_null(CollectionConnection), graphql_name='collections', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(CollectionSortKeys, graphql_name='sortKey', default='ID')),
        ('query', types.Arg(String, graphql_name='query', default=None)),
        ('saved_search_id', types.Arg(ID, graphql_name='savedSearchId', default=None)),
    )))

    node = types.Field(Node, graphql_name='node', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    nodes = types.Field(types.non_null(types.list_of(Node)), graphql_name='nodes', args=types.ArgDict((
        ('ids', types.Arg(types.non_null(types.list_of(types.non_null(ID))), graphql_name='ids', default=None)),
    )))
    private_metafield = types.Field('PrivateMetafield', graphql_name='privateMetafield', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    private_metafields = types.Field(types.non_null(PrivateMetafieldConnection), graphql_name='privateMetafields', args=types.ArgDict((
        ('namespace', types.Arg(String, graphql_name='namespace', default=None)),
        ('owner', types.Arg(types.non_null(ID), graphql_name='owner', default=None)),
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
    )))
    product = types.Field('Product', graphql_name='product', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    product_variant = types.Field('ProductVariant', graphql_name='productVariant', args=types.ArgDict((
        ('id', types.Arg(types.non_null(ID), graphql_name='id', default=None)),
    )))
    product_variants = types.Field(types.non_null(ProductVariantConnection), graphql_name='productVariants', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(ProductVariantSortKeys, graphql_name='sortKey', default='ID')),
        ('query', types.Arg(String, graphql_name='query', default=None)),
        ('saved_search_id', types.Arg(ID, graphql_name='savedSearchId', default=None)),
    )))
    products = types.Field(types.non_null(ProductConnection), graphql_name='products', args=types.ArgDict((
        ('first', types.Arg(Int, graphql_name='first', default=None)),
        ('after', types.Arg(String, graphql_name='after', default=None)),
        ('last', types.Arg(Int, graphql_name='last', default=None)),
        ('before', types.Arg(String, graphql_name='before', default=None)),
        ('reverse', types.Arg(Boolean, graphql_name='reverse', default=False)),
        ('sort_key', types.Arg(ProductSortKeys, graphql_name='sortKey', default='ID')),
        ('query', types.Arg(String, graphql_name='query', default=None)),
        ('saved_search_id', types.Arg(ID, graphql_name='savedSearchId', default=None)),
    )))


class Mutation(types.Type):
    pass


########################################################################
# Schema Entry Points
########################################################################
shopify_schema.query_type = QueryRoot
shopify_schema.mutation_type = Mutation
shopify_schema.subscription_type = None
