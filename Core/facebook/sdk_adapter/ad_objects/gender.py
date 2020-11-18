from enum import Enum

from facebook_business.adobjects.serverside import gender

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum, Contexts

_gender = gender.Gender


@cat_enum
class Gender(Enum):
    MALE = Cat(_gender.MALE.value)
    FEMALE = Cat(_gender.FEMALE.value)


@cat_enum
class GenderGroup(Enum):
    ALL = Cat(None, _gender.FEMALE.value, _gender.MALE.value)
    MEN = Cat(None, _gender.MALE.value)
    WOMEN = Cat(None, _gender.FEMALE.value)

    contexts = Contexts.all_with_items(ALL, MEN, WOMEN, default_item=ALL)
