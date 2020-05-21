from facebook_business.adobjects.application import Application

from Core.Tools.Misc.EnumerationBase import EnumerationBase


class GraphAPIAppFields(EnumerationBase):
    APP_NAME = Application.Field.app_name
    APP_TYPE = Application.Field.app_type
    CATEGORY = Application.Field.category
    CREATED_TIME = Application.Field.created_time
    DESCRIPTION = Application.Field.description
    ID = Application.Field.id
    NAME = Application.Field.name
