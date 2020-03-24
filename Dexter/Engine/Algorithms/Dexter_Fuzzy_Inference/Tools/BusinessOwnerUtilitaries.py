import math
from Algorithms.Models.Types import TypesWrapper
from Algorithms.Tools.RemoveActorPrefix import remove_actor_prefix

def get_accounts_for_bo(business_owner_facebook_id, data):

    for element in data:
        if element['business_owner_facebook_id'] == business_owner_facebook_id:
            return [remove_actor_prefix(account_id) for account_id in element['ad_account_ids']]

def get_number_of_actors_per_business_account(business_owners_data):

    number_of_actors_per_business_account = dict()

    for business_owner in business_owners_data:
        business_owner_id = business_owner['business_owner_facebook_id']
        number_of_actors_per_business_account[business_owner_id] = len(business_owner['ad_account_ids'])

    return number_of_actors_per_business_account


def get_data_for_account_id(ad_account_id, mongo_repository, all_insights_collections):

    resulting_insights = []
    for collection in all_insights_collections:
        mongo_repository.collection = collection
        level = collection.split('-')[0]
        breakdown = collection.split('-')[1]
        action_breakdown = collection.split('-')[2]

        combination = TypesWrapper.OptimizationTuple(level, breakdown, action_breakdown)

        collection_data_for_ad_account = mongo_repository.get_all_by_key(key="account_id", values=[ad_account_id])
        actual_insights = []
        for insight in collection_data_for_ad_account:
            # TODO: check when google comes if htis is still a thing
            if insight['date_start'] is None or insight['date_stop'] is None:
                pass
            else:
                actual_insights.append(insight)

        resulting_insights.append((actual_insights, combination))

    return resulting_insights