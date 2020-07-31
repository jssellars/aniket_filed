import typing
from dataclasses import dataclass


@dataclass
class Product:
    id: typing.AnyStr = None
    currency: typing.AnyStr = None
    description: typing.AnyStr = None
    url: typing.AnyStr = None
    details: typing.Dict = None
    availability: typing.AnyStr = None
    name: typing.AnyStr = None
    price: typing.AnyStr = None
    facebook_product_group_id: typing.AnyStr = None
    category: typing.AnyStr = None
    type: typing.AnyStr = None
    short_description: typing.AnyStr = None
    custom_data: typing.Dict = None
    custom_label_0: typing.AnyStr = None
    custom_label_1: typing.AnyStr = None
    custom_label_2: typing.AnyStr = None
    custom_label_3: typing.AnyStr = None
    custom_label_4: typing.AnyStr = None
