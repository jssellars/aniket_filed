import math
from datetime import datetime, timedelta
from enum import Enum

import requests

from Algorithms.Tools.Columns import StructuresCollectionNames
from Packages.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Packages.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Startup import startup


class MetricsVariationsEnum(Enum):
    RESULTS_DECREASE_PERCENT = 'results_decrease_percent'
    CPM_INCREASE_PERCENT = 'cpm_increase_percent'
    CPC_INCREASE_PERCENT = 'cpc_increase_percent'
    LINK_CLICKS_DECREASE_PERCENT = 'link_clicks_decrease_percent'
    FREQUENCY_DECREASE_PERCENT = 'frequency_decrease_percent'
    REACH_CURRENT_VALUE = 'reach_current_value'
    ROAS_CURRENT_VALUE = 'roas_current_value'
    INTERESTS = 'interests'


class TimePeriod(Enum):
    WEEK = timedelta(days=7)
    THREE_DAYS = timedelta(days=3)


class TemplateInfoFactory:
    @staticmethod
    def __inorder_traversal(node, accumulator):
        if 'children' in node:
            for children in node['children']:
                TemplateInfoFactory.__inorder_traversal(children, accumulator)
        else:
            accumulator.append((node['name'], node['audience_size']))

    @staticmethod
    def get_info_for_keywords(keywords, data):
        keyword_value_tuples = []
        for keyword in keywords:
            information_for_keyword = TemplateInfoFactory.process_keyword(keyword, data)
            if information_for_keyword:
                keyword_value_tuples.append((keyword, information_for_keyword))

        return keyword_value_tuples

    @staticmethod
    def __calculate_percentage_last_3_days_for_metric(data, metric, decreasing=True):

        last_date = datetime.strptime(data[len(data) - 1]['date_start'], '%Y-%m-%d')
        first_date = datetime.strptime(data[0]['date_start'], '%Y-%m-%d')
        days = last_date - first_date
        days = days.days
        observed_values = [x[metric] for x in data]
        observed_values = list(map(lambda x: x if x is not None else 0, observed_values))
        mean_value = sum(observed_values) / days
        mean_last_3_values = sum(observed_values[-3:]) / 3

        if decreasing:
            return math.floor((1 - mean_last_3_values / mean_value) * 100)
        else:
            return math.floor((mean_last_3_values / mean_value - 1) * 100)

    @staticmethod
    def process_keyword(keyword, data):

        # TODO: For the moment, Dexter is considering gaps between data samples to be null or 0.
        # TODO: Work up a way to make that be the correct approach
        # TODO: E.g. If I have a variation of 10 days but I have data only for 5, the rest of 5 is considered to be 0.

        if keyword == MetricsVariationsEnum.RESULTS_DECREASE_PERCENT.value:
            return TemplateInfoFactory.__calculate_percentage_last_3_days_for_metric(data, metric='results', decreasing=True)

        elif keyword == MetricsVariationsEnum.CPM_INCREASE_PERCENT.value:
            return TemplateInfoFactory.__calculate_percentage_last_3_days_for_metric(data, metric='cpm', decreasing=False)

        elif keyword == MetricsVariationsEnum.CPC_INCREASE_PERCENT.value:
            return TemplateInfoFactory.__calculate_percentage_last_3_days_for_metric(data, metric='cpc', decreasing=False)

        elif keyword == MetricsVariationsEnum.LINK_CLICKS_DECREASE_PERCENT.value:
            return TemplateInfoFactory.__calculate_percentage_last_3_days_for_metric(data, metric='link_click', decreasing=True)

        elif keyword == MetricsVariationsEnum.FREQUENCY_DECREASE_PERCENT.value:
            return TemplateInfoFactory.__calculate_percentage_last_3_days_for_metric(data, metric='frequency', decreasing=True)

        elif keyword == MetricsVariationsEnum.REACH_CURRENT_VALUE.value:
            for item_data in reversed(data):
                if item_data['reach']:
                    return item_data['reach']

        elif keyword == MetricsVariationsEnum.ROAS_CURRENT_VALUE.value:
            # we basically return the LAST known value. not the current
            for item_data in reversed(data):
                if item_data['website_purchase_roas']:
                    return math.floor(item_data['website_purchase_roas'])

        elif keyword == MetricsVariationsEnum.INTERESTS.value:
            interests = []
            adset_id = data['adset_id']

            mongo_structures_connection_config = MongoConnectionHandler(mongo_config=startup.mongoConfig)
            mongo_client_structures = mongo_structures_connection_config.client

            mongo_structures_getter = MongoRepositoryBase(client=mongo_client_structures, database_name=startup.mongoConfig.structuresDatabaseName)
            mongo_structures_getter.collection = StructuresCollectionNames.ADSET.value

            structure = mongo_structures_getter.get_all_by_key('adset_id', [adset_id])[0]
            if 'details' in structure:
                if 'targeting' in structure['details']:
                    if 'flexible_spec' in structure['details']['targeting']:
                        if 'interests' in structure['details']['targeting']['flexible_spec']:
                            interests = structure['details']['targeting']['flexible_spec']['interests']

            print('I am in interests {}'.format(interests))

            endpoint = 'https://targetingsearch.filed.com/interests/suggestions/'
            if interests:
                interests = [interest['name'] for interest in interests]
                endpoint += ','.join(interests)

                result = requests.get(url=endpoint)
                result = result.json()
                results_root = result['results']
                interests_accumulator = []
                for result in results_root:
                    TemplateInfoFactory.__inorder_traversal(node=result, accumulator=interests_accumulator)

                top_5_interests = list(list(sorted(interests_accumulator, key=lambda x: x[1] if x[1] is not None else 0, reverse=True))[:5])
                top_5_interests = list(map(lambda x: x[0], top_5_interests))

                print(', '.join(top_5_interests))

                return ', '.join(top_5_interests)

        # TODO: These either do not have data, or can't be done now
        elif keyword == 'conversation_rate_percent_decrease_week':
            # TODO: how do you calculate the conversion rate?
            pass
        elif keyword == 'cost_per_result_week':
            # TODO: does not exist in current insights
            pass
        elif keyword == 'cost_per_play_increase':
            # TODO: does not exist in current insights
            pass
        elif keyword == 'cost_per_install_increase':
            # TODO: does not exist in current insights
            pass

        return None
