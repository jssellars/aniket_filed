from operator import itemgetter

from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerCampaignTreeStructureQuery:
    class CampaignKeyMap:
        id = "campaign_id"
        name = "campaign_name"

    class AdSetKeyMap:
        id = "adset_id"
        name = "adset_name"

    class AdKeyMap:
        id = "ad_id"
        name = "ad_name"

    keymap = {
        Level.CAMPAIGN.value: CampaignKeyMap,
        Level.ADSET.value: AdSetKeyMap,
        Level.AD.value: AdKeyMap
    }

    @classmethod
    def get(cls, level, facebook_id):
        repository = TuringMongoRepository(config=startup.mongo_config,
                                           database_name=startup.mongo_config['structures_database_name'],
                                           collection_name=level)
        try:
            structure = repository.get_active_structure_ids(cls.keymap[level].id, facebook_id)
            campaign_id = list(map(itemgetter(cls.keymap[Level.CAMPAIGN.value].id), structure))
            campaign_id = campaign_id[0]
        except Exception as e:
            raise e

        try:
            structures = {}
            for structure_level in Level:
                if structure_level != Level.ACCOUNT:
                    repository.collection = structure_level.value
                    structures[structure_level.value] = repository.get_active_structure_ids(cls.keymap[Level.CAMPAIGN.value].id,
                                                                                            campaign_id)
        except Exception as e:
            raise e

        try:
            tree = {
                "id": structures[Level.CAMPAIGN.value][0][cls.keymap[Level.CAMPAIGN.value].id],
                "name": structures[Level.CAMPAIGN.value][0][cls.keymap[Level.CAMPAIGN.value].name],
                "children": [{
                    "id": structure[cls.keymap[Level.ADSET.value].id],
                    "name": structure[cls.keymap[Level.ADSET.value].name],
                    "children": list(map(cls.build_ad_leaf,
                                         filter(lambda x: x[cls.keymap[Level.ADSET.value].id] == structure[
                                             cls.keymap[Level.ADSET.value].id],
                                                structures[Level.AD.value]
                                                )
                                         )
                                     )
                } for structure in structures[Level.ADSET.value]]}
        except Exception as e:
            raise e

        return tree

    @classmethod
    def build_ad_leaf(cls, ad):
        return {"id": ad[cls.keymap[Level.AD.value].id],
                "name": ad[cls.keymap[Level.AD.value].name]}
