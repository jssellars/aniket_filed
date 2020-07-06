from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from FacebookDexter.Api.Config.Config import MongoConfig
import pymongo
from FacebookDexter.Api.Models.Domain.Recommendation import Recommendation
from FacebookDexter.Api.Models.Domain.RecommendationType import RecommendationType
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from FacebookDexter.Api.Models.Domain.RecommendationCategory import RecommendationCategory
from datetime import datetime
from bson import ObjectId
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from FacebookDexter.Api.Models.Domain.RecommendationFields import RecommendationField
import copy


class RecommendationsRepository(MongoRepositoryBase):

    def __init__(self, config: MongoConfig):
        super().__init__(config=config)
        self.database = config['recommendation_database_name']
        self.collection = config['recommendation_collection_name']

    def get_campaigns(self, ad_account_id, channel):
        aggregation = [

            {MongoOperator.MATCH.value: {
                RecommendationField.AD_ACCOUNT_ID.value: ad_account_id,
                RecommendationField.CHANNEL.value: channel,
                RecommendationField.CONFIDENCE.value: {MongoOperator.GREATERTHANEQUAL.value: 0.5},
                RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value
            }
            },
            {MongoOperator.GROUP.value: {
                MongoOperator.GROUP_KEY.value: {
                    RecommendationField.CAMPAIGN_ID.value: "$campaign_id",
                    RecommendationField.CAMPAIGN_NAME.value: "$campaign_name",
                    RecommendationField.CHANNEL.value: '$channel',
                    RecommendationField.AD_ACCOUNT_ID.value: '$ad_account_id'
                }
            }
            }
        ]
        cursor = self.collection.aggregate(aggregation)
        campaigns = list(cursor)
        distinct_campaigns = [{'id': campaign[MongoOperator.GROUP_KEY.value][RecommendationField.CAMPAIGN_ID.value],
                               'name': campaign[MongoOperator.GROUP_KEY.value][RecommendationField.CAMPAIGN_NAME.value]}
                              for campaign in campaigns]
        return distinct_campaigns

    def get_recommendation_by_id(self, id: str):
        try:
            recommendation = self.collection.find_one(
                {RecommendationField.OBJECT_ID.value: ObjectId(id),
                 RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value
                 })

        # The id string may not be a valid string for ObjectId. In this case,  ObjectId(id) will raise an exception.
        # Return None in this just as if the recommendation does not exist
        except Exception as e:
            return None

        if recommendation is not None:
            return Recommendation(recommendation).__dict__
        return None

    def get_recommendations_page(self, page_number, page_size, recommendation_filter=None, recommendation_sort=None,
                                 excluded_ids=None):
        skipped = (page_number - 1) * page_size
        query_sort = [(RecommendationField.CREATED_AT.value, pymongo.DESCENDING)]
        if recommendation_sort is not None:
            query_sort = recommendation_sort
        if excluded_ids is None:
            excluded_ids = []

        cursor, count = self.get_recommendations(recommendation_filter, excluded_ids)
        recommendations = list(cursor.sort(query_sort).skip(skipped).limit(page_size))
        recommendations_as_dict_list = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in
                                        recommendations]
        response_dict = {'count': count, 'recommendations': recommendations_as_dict_list}
        counts_filter = {}
        if recommendation_filter is not None:
            if RecommendationField.CAMPAIGN_ID.value in recommendation_filter:
                counts_filter[RecommendationField.CAMPAIGN_ID.value] = {
                    MongoOperator.IN.value: recommendation_filter[RecommendationField.CAMPAIGN_ID.value]}
        counts_by_type = self.get_counts_by_type(counts_filter)
        response_dict['countsByType'] = counts_by_type
        return response_dict

    def set_recommendation_statuses_by_structure_id(self, structure_id, status):
        now = datetime.now()
        return self.collection.update_many(
            {RecommendationField.STRUCTURE_ID.value: structure_id,
             RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value},
            {MongoOperator.SET.value: {
                RecommendationField.STATUS.value: status,
                RecommendationField.APPLICATION_DATE.value: now,
                RecommendationField.APPLIED_BY.value: 'Dexter'}})

    def set_recommendation_status(self, recommendation_id: str, status: str):
        recommendation_object_id = ObjectId(recommendation_id)
        now = datetime.now()
        self.collection.update_one({RecommendationField.OBJECT_ID.value: recommendation_object_id},
                                   {MongoOperator.SET.value: {
                                       RecommendationField.STATUS.value: status,
                                       RecommendationField.APPLICATION_DATE.value: now,
                                       RecommendationField.APPLIED_BY.value: 'Dexter'}})
        return Recommendation(self.collection.find_one({RecommendationField.OBJECT_ID.value: recommendation_object_id})).__dict__

    def get_action_history(self, structure_id: str):
        cursor = self.collection.find(
            {RecommendationField.STRUCTURE_ID.value: structure_id,
             RecommendationField.STATUS.value:
                {MongoOperator.IN.value: [RecommendationStatusEnum.APPLIED.value,
                                          RecommendationStatusEnum.DISMISSED.value]}},
            {RecommendationField.APPLICATION_DETAILS.value: False}).sort(RecommendationField.APPLICATION_DATE.value, pymongo.DESCENDING)
        action_histories_as_dict_list = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in
                                         list(cursor)]
        return action_histories_as_dict_list

    def get_recommendations(self, recommendation_filter=None, excluded_ids=None):
        query_filter = {}
        if recommendation_filter is not None:
            for key in recommendation_filter:
                if key == 'search_term':
                    search_filter = {'$regex': filter[key],
                                     '$options': 'i'}  # ignore case
                    query_filter[RecommendationField.STRUCTURE_NAME.value] = search_filter
                    continue
                if isinstance(recommendation_filter[key], list):
                    query_filter[key] = {MongoOperator.IN.value: recommendation_filter[key]}
                else:
                    query_filter[key] = recommendation_filter[key]

        if excluded_ids is not None:
            query_filter[RecommendationField.OBJECT_ID.value] = {MongoOperator.NOTIN.value: [ObjectId(excluded_id) for excluded_id in excluded_ids]}
        query_filter[RecommendationField.STATUS.value] = RecommendationStatusEnum.ACTIVE.value

        projection = {RecommendationField.APPLIED_BY.value: False,
                      RecommendationField.APPLICATION_DATE.value: False,
                      RecommendationField.STATUS.value: False}
        count = self.get_count_by_filter(query_filter)
        response = self.collection.find(query_filter, projection)
        return response, count

    def get_counts_by_type(self, recommendation_filter):
        counts_by_type = {}
        match_filter = copy.deepcopy(recommendation_filter)
        match_filter[RecommendationField.STATUS.value] = RecommendationStatusEnum.ACTIVE.value
        match_filter[RecommendationField.CONFIDENCE.value] = {MongoOperator.GREATERTHANEQUAL.value: 0.5}
        match_aggregation = {MongoOperator.MATCH.value: match_filter}
        count_aggregation = {MongoOperator.GROUP.value: {
            MongoOperator.GROUP_KEY.value: '$recommendation_type',
            'count': {MongoOperator.SUM.value: 1}
        }}

        aggregation = [match_aggregation, count_aggregation]
        cursor = self.collection.aggregate(aggregation)
        counts = list(cursor)

        for reco_type in RecommendationType:
            type_count = 0
            for count in counts:
                if count[MongoOperator.GROUP_KEY.value] == reco_type.value:
                    type_count = count['count']

            counts_by_type[reco_type.value] = type_count

        return counts_by_type

    def get_counts_by_category(self, recommendation_filter):
        counts_by_category = {}
        match_filter = copy.deepcopy(recommendation_filter)
        match_filter[RecommendationField.STATUS.value] = RecommendationStatusEnum.ACTIVE.value
        match_filter[RecommendationField.CONFIDENCE.value] = {MongoOperator.GREATERTHANEQUAL.value: 0.5}
        match_aggregation = {MongoOperator.MATCH.value: match_filter}
        count_aggregation = {MongoOperator.GROUP.value: {
            MongoOperator.GROUP_KEY.value: '$category',
            'count': {MongoOperator.SUM.value: 1}
        }}

        aggregation = [match_aggregation, count_aggregation]
        cursor = self.collection.aggregate(aggregation)
        counts = list(cursor)

        for metric in RecommendationCategory:
            metric_count = 0
            for count in counts:
                if count[MongoOperator.GROUP_KEY.value] == metric.value:
                    metric_count = count['count']

            counts_by_category[metric.value] = metric_count
        return counts_by_category

    def get_counts(self, recommendation_filter):
        types = self.get_counts_by_type(recommendation_filter)
        metrics = self.get_counts_by_category(recommendation_filter)
        types.update(metrics)
        return types

    def get_count_by_filter(self, recommendation_filter=None):
        count_filter = {}
        if recommendation_filter is not None:
            count_filter = recommendation_filter
        count = self.collection.count_documents(count_filter)
        return count
