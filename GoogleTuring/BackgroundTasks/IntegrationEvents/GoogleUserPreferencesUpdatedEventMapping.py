from marshmallow import fields, EXCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase, MapperNestedField
from GoogleTuring.BackgroundTasks.IntegrationEvents.GoogleUserPreferencesUpdatedEvent import Customer


class GoogleUserPreferencesUpdatedEventMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    google_id = fields.String()
    email_address = fields.String()
    refresh_token = fields.String()
    customers = MapperNestedField(target=Customer, many=True)
