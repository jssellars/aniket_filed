from Potter.FacebookCampaignsBuilder.Api.Catalogs.CampaignBidStrategyCatalog import CampaignBidStrategyCatalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import ObjectivesCatalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.SpecialAdCategoryCatalog import SpecialAdCategoryCatalog


class SmartCreateCatalogsQuery:
    def get(self):
        special_ad_category = SpecialAdCategoryCatalog()

        objectives = ObjectivesCatalog()

        campaign_bid = CampaignBidStrategyCatalog()

        all_catalogs = {'SpecialAdCategory': special_ad_category.to_json(),
                        'Objectives': objectives.to_json(),
                        'BidStrategy': campaign_bid.to_json()}
        return all_catalogs
