from enum import Enum

from facebook_business.adobjects.serverside import gender

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

_gender = gender.Gender


@cat_enum
class Gender(Enum):
    MALE = Cat(_gender.MALE.value)
    FEMALE = Cat(_gender.FEMALE.value)
