from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from GoogleTuring.Api.Catalogs.BusinessViews.ViewAd import ViewAd
from GoogleTuring.Api.Catalogs.BusinessViews.ViewAdGroup import ViewAdGroup, ViewAdGroupKeywords, ViewAdGroupGender, ViewAdGroupAge
from GoogleTuring.Api.Catalogs.BusinessViews.ViewCampaign import ViewCampaign, ViewCampaignGender, ViewCampaignKeywords, ViewCampaignAge


class AdsManagerCatalogsViewsByLevelDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    campaign = [
        ViewCampaign(),
        ViewCampaignKeywords(),
        ViewCampaignGender(),
        ViewCampaignAge()
    ]

    ad_group = [
        ViewAdGroup(),
        ViewAdGroupKeywords(),
        ViewAdGroupGender(),
        ViewAdGroupAge()
    ]

    ad = [
        ViewAd(),
    ]

    def __init__(self):
        super().__init__()

    @classmethod
    def get(cls, level):
        return cls.json_encoder(getattr(cls, level))
