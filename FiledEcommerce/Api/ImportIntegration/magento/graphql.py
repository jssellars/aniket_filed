from sgqlc.types import Enum, non_null, Arg, String, Float, Type, Int, Field, list_of, Boolean, ArgDict ,Interface, Union, Input, Schema
from sgqlc import types

magento_schema = Schema()

class CurrencyEnum(Enum):
    __schema__ = magento_schema
    __choices__ = ('EUR', 'USD')

class ProductStockStatus(Enum):
    __schema__ = magento_schema
    __choices__ = ('IN_STOCK', 'OUT_OF_STOCK')

class ComplexTextValue(Type):
    __schema__ = magento_schema
    __field_names__ = ('html',)
    html = Field(String, graphql_name ='html')

class Breadcrumbs(Type):
    __schema__ = magento_schema
    __field_names__ = ('category_id', 'category_level', 'category_name', 'category_url_key')
    category_id = Field(Int, graphql_name='category_id')
    category_level= Field(Int, graphql_name='category_level')
    category_name = Field(String, graphql_name='category_name')
    category_url_key= Field(String, graphql_name='category_url_key')

class CategoryInterface(Type):
    #https://devdocs.magento.com/guides/v2.3/graphql/interfaces/category-interface.html
    __schema__ = magento_schema
    __field_names__ = (
    'breadcrumbs',
    'description',
    'id',
    'level',
    'name',
    'path_in_store',
    'path',
    'product_count',
    'updated_at',
    'url_key',
    'url_path'
    )
    breadcrumbs= Field(Breadcrumbs, graphql_name='breadcrumbs')
    description = Field(String, graphql_name='description')
    id = Field(non_null(Int), graphql_name='id')
    level = Field(Int, graphql_name='level')
    name = Field(String, graphql_name='name')
    path_in_store = Field(String, graphql_name='path_in_store')
    path = Field(String, graphql_name='path')
    product_count = Field(Int, graphql_name='product_count')
    updated_at = Field(String, graphql_name='updated_at')
    url_key = Field(String, graphql_name='url_key')
    url_path = Field(String, graphql_name='url_path')

class SearchResultPageInfo(Type):
    __schema__ = magento_schema
    __field_names__ = ('page_size','current_page','total_pages')
    page_size = Field(Int, graphql_name='page_size')
    current_page = Field(Int, graphql_name='current_page')
    total_pages= Field(Int, graphql_name='total_pages')

class Money(Type):
    __schema__ = magento_schema
    __field_names__ = ('currency','value')
    currency = Field(CurrencyEnum, graphql_name='currency')
    value = Field(Float, graphql_name='value')

class Price(Type):
    __schema__ = magento_schema
    __field_names__ = ('amount',)
    amount = Field(Money, graphql_name='amount')
    
class ProductPrices(Type):
    # https://devdocs.magento.com/guides/v2.3/graphql/interfaces/product-interface.html#PriceRange
    __schema__ = magento_schema
    __field_names__ = ('maximalPrice','minimalPrice','regularPrice')
    maximalPrice = Field(Price, graphql_name='maximalPrice')
    minimalPrice = Field(Price, graphql_name='minimalPrice')
    regularPrice = Field(Price, graphql_name='regularPrice')    

class ProductImage(Type):
    __schema__ = magento_schema
    __field_names__ = ('label','url')
    label = Field(String, graphql_name='label') 
    url = Field(String, graphql_name='url') 

class MagentoProductVariant(Type):
    __schema__ = magento_schema
    __field_names__ = (
        'id', 
        'name', 
        'sku', 
        'attribute_set_id',
        'meta_keyword', 
        'canonical_url',  
        'created_at', 
        'updated_at', 
        'description', 
        'image',  
        'price',  
        'stock_status', 
    )
    id = Field(non_null(Int), graphql_name='id')
    name = Field(non_null(String), graphql_name='name')
    meta_keyword = Field(String, graphql_name='meta_keyword')
    sku = Field(non_null(String), graphql_name='sku')
    stock_status = Field(ProductStockStatus, graphql_name='stock_status')
    attribute_set_id = Field(Int, graphql_name='attribute_set_id')  
    canonical_url = Field(non_null(String), graphql_name='canonical_url')
    created_at = Field(String, graphql_name='created_at')
    updated_at = Field(String, graphql_name='updated_at')
    image = Field(ProductImage, graphql_name='image')
    price = Field(ProductPrices, graphql_name='price')
    description = Field(ComplexTextValue, graphql_name='description')

class ProductInterface(Type):
    #https://devdocs.magento.com/guides/v2.3/graphql/interfaces/product-interface.html
    __schema__ = magento_schema
    __field_names__ = (
        'id', 
        'name', 
        'sku', 
        'attribute_set_id', 
        'canonical_url', 
        'categories', 
        'country_of_manufacture',
        'meta_keyword', 
        'created_at', 
        'updated_at', 
        'description', 
        'image', 
        'manufacturer', 
        'options_container', 
        'price', 
        'short_description', 
        'small_image', 
        'stock_status', 
        'thumbnail',
        'only_x_left_in_stock'
    )
    id = Field(non_null(Int), graphql_name='id')
    name = Field(non_null(String), graphql_name='name')
    sku = Field(non_null(String), graphql_name='sku')
    attribute_set_id = Field(Int, graphql_name='attribute_set_id')
    canonical_url = Field(non_null(String), graphql_name='canonical_url')
    categories= Field(list_of(CategoryInterface), graphql_name='categories')
    country_of_manufacture= Field(String, graphql_name='country_of_manufacture')
    meta_keyword= Field(String, graphql_name='meta_keyword')
    created_at = Field(String, graphql_name='created_at')
    updated_at = Field(String, graphql_name='updated_at')
    description = Field(ComplexTextValue, graphql_name='description')
    image = Field(ProductImage, graphql_name='image')
    manufacturer= Field(String, graphql_name='manufacturer')
    options_container = Field(String, graphql_name='options_container')
    price = Field(ProductPrices, graphql_name='price')
    short_description = Field(ComplexTextValue, graphql_name='short_description')
    small_image = Field(ProductImage, graphql_name='small_image')
    stock_status = Field(ProductStockStatus, graphql_name='stock_status')
    thumbnail = Field(ProductImage, graphql_name='thumbnail')
    only_x_left_in_stock = Field(Float, graphql_name='only_x_left_in_stock')

class Attributes(Type):
    __schema__ = magento_schema
    __field_names__ = ('label', 'code', 'value_index')   
    label = Field(String, graphql_name='label')
    code = Field(String, graphql_name='code')
    value_index = Field(Int, graphql_name='value_index')

class Variants(Type):
    __schema__ = magento_schema
    __field_names__ = ('product', 'attributes')   
    attributes = Field(Attributes, graphql_name='attributes')
    product = Field(MagentoProductVariant, graphql_name='product')

class ConfigurableProductOptionsValues(Type):
    __schema__ = magento_schema
    __field_names__ = ('label', 'store_label', 'value_index')  
    label =  Field(String, graphql_name='label')
    store_label = Field(String, graphql_name='store_label')
    value_index = Field(Int, graphql_name='value_index')

class ConfigurableProductOptions(Type):
    __schema__ = magento_schema
    __field_names__ = (
    'id', 
    'attribute_code', 
    'attribute_id',
    'label',
    'position',
    'product_id',
    'use_default',
    'values'
    ) 
    id = Field(Int, graphql_name='id')
    attribute_code = Field(String, graphql_name='attribute_code')
    attribute_id = Field(String, graphql_name='attribute_id')
    label = Field(String, graphql_name='label')
    position = Field(Int, graphql_name='position')
    product_id = Field(Int, graphql_name='product_id')
    use_default = Field(Boolean, graphql_name='use_default')
    values = Field(list_of(ConfigurableProductOptionsValues), graphql_name='values')

class ConfigurableProduct(Type):
    __schema__ = magento_schema
    __field_names__ = ('configurable_options', 'variants')  
    configurable_options= Field(ConfigurableProductOptions, graphql_name='configurable_options')
    variants = Field(Variants, graphql_name='variants')

class FilterMatchTypeInput(Type):
    __schema__ = magento_schema
    __field_names__ = ('match',)   
    match = Field(String, graphql_name='match')

class ProductAttributeFilterInput(Input):
    __schema__ = magento_schema
    __field_names__ = ('name',)  
    name = Field(FilterMatchTypeInput, graphql_name='name')

class Product(Type):
    __schema__ = magento_schema
    __field_names__ = ('items', 'total_count', 'page_info') 
    items = Field(ProductInterface, graphql_name='items')
    total_count = Field(Int, graphql_name='total_count')
    page_info = Field(SearchResultPageInfo, graphql_name='page_info')

class MagentoQuery(Type):
    __schema__ = magento_schema
    __field_names__ = ('products',) 
    products = Field(Product, args = ArgDict(
            ('filter', Arg(ProductAttributeFilterInput, graphql_name='filter', default=None)),
            ('pageSize', Arg(Int, graphql_name='pageSize', default=None)),
            ('currentPage', Arg(Int, graphql_name='currentPage', default=None)),
        ))

########################################################################
# Schema Entry Points
########################################################################

magento_schema.query_type = MagentoQuery
