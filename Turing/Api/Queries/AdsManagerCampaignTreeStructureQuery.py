from operator import itemgetter

from Turing.Api.Startup import startup
from Turing.Infrastructure.Mappings.LevelMapping import Level
from Turing.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerCampaignTreeStructureQuery:

    class CampaignKeyMap:
        id = "campaign_id"
        name = "campaign_name"

    class AdSetKeyMap:
        id = "adset_id"
        name = "adset_name"

    class AdKeyMap:
        id = "ad_id"
        name = "name"

    keymap = {
        Level.CAMPAIGN.value: CampaignKeyMap,
        Level.ADSET.value: AdSetKeyMap,
        Level.AD.value: AdKeyMap
    }

    @classmethod
    def get(cls, level, facebook_id):
        # todo: check why ads are not returned in "children" per adset
        mongo_repository = TuringMongoRepository(config=startup.mongo_config,
                                                 database_name=startup.mongo_config['structures_database_name'],
                                                 collection_name=level)

        structure = mongo_repository.get_all_by_key(cls.keymap[level].id, [facebook_id])

        campaign_id = list(map(itemgetter(cls.keymap[Level.CAMPAIGN.value].id), structure))

        structures = {}
        for structure_level in Level:
            if structure_level != Level.ACCOUNT:
                mongo_repository.collection = structure_level.value
                structures[structure_level.value] = mongo_repository.get_all_by_key(cls.keymap[Level.CAMPAIGN.value].id, campaign_id)

        tree = {
            "id": structures[Level.CAMPAIGN.value][0][cls.keymap[Level.CAMPAIGN.value].id],
            "name": structures[Level.CAMPAIGN.value][0][cls.keymap[Level.CAMPAIGN.value].name],
            "children": [{
                "id": structure[cls.keymap[Level.ADSET.value].id],
                "name": structure[cls.keymap[Level.ADSET.value].name],
                "children": list(map(cls.build_ad_leaf,
                                     filter(lambda x: x[cls.keymap[Level.ADSET.value].id] == structure[cls.keymap[Level.ADSET.value].id],
                                            structures[Level.AD.value]
                                            )
                                     )
                                 )
            } for structure in structures[Level.ADSET.value]]}

        return tree

    @classmethod
    def build_ad_leaf(cls, ad):
        return {"id": ad[cls.keymap[Level.AD.value].id],
                "name": ad[cls.keymap[Level.AD.value].name]}
