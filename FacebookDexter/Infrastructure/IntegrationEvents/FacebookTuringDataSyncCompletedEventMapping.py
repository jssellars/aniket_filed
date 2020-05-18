from marshmallow import EXCLUDE, fields

from Core.Tools.Mapper.MapperBase import MapperBase


class FacebookTuringDataSyncCompletedEventMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    business_owner_facebook_id = fields.String()
    ad_account_ids = fields.List(fields.String())
