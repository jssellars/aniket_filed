from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.BusinessViews.ViewCampaignPerformances import ViewCampaignPerformances, ViewCampaignGender
from GoogleTuring.Api.Catalogs.BusinessViews.ViewAdGroup import ViewAdGroup, ViewAdGroupGender


class AdsManagerCatalogsViewsByLevelDto:

    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    campaign = [
        ViewCampaignPerformances(),
        ViewCampaignGender()
    ]

    ad_group = [
        ViewAdGroup(),
        ViewAdGroupGender()
    ]

    ad = []

    def __init__(self):
        super().__init__()

    @classmethod
    def get(cls, level):
        return cls.json_encoder(getattr(cls, level))
