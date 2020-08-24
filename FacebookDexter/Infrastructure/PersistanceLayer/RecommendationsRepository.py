import copy
from datetime import datetime

import pymongo
from bson import ObjectId
from pymongo.errors import AutoReconnect
from retry import retry

from Core.Dexter.Infrastructure.Domain.Recommendations.Recommendation import Recommendation
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Core.Tools.Logger.Helpers import log_operation_mongo
from FacebookDexter.Api.Config.Config import MongoConfig
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationCategory import RecommendationCategory
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationType import RecommendationType


class RecommendationsRepository(MongoRepositoryBase):

    __RETRY_LIMIT = 3

    def __init__(self, config: MongoConfig, **kwargs):
        super().__init__(config=config, **kwargs)
        self.database = config['recommendations_database_name']
        self.collection = config['recommendations_collection_name']

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
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

        operation_start_time = datetime.now()

        try:
            cursor = self.collection.aggregate(aggregation)
            campaigns = list(cursor)
            distinct_campaigns = [{'id': campaign[MongoOperator.GROUP_KEY.value][RecommendationField.CAMPAIGN_ID.value],
                                   'name': campaign[MongoOperator.GROUP_KEY.value][RecommendationField.CAMPAIGN_NAME.value]}
                                  for campaign in campaigns]
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to get campaigns with recommendations. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=aggregation)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                data=distinct_campaigns,
                                description='Get campaigns with recommendations',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=aggregation)

        return distinct_campaigns

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_recommendation_by_id(self, recommendation_id: str):
        query = {RecommendationField.OBJECT_ID.value: ObjectId(recommendation_id),
                 RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value
                 }
        operation_start_time = datetime.now()
        try:
            recommendation = self.collection.find_one(query)

        # The id string may not be a valid string for ObjectId. In this case,  ObjectId(id) will raise an exception.
        # Return None in this just as if the recommendation does not exist
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to get campaigns with recommendations. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                data=recommendation,
                                description='Get campaigns with recommendations',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query)

        if recommendation is not None:
            return Recommendation(recommendation).__dict__
        return None

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_recommendations_page(self, page_number, page_size, recommendation_filter=None, recommendation_sort=None,
                                 excluded_ids=None):
        skipped = (page_number - 1) * page_size
        query_sort = [(RecommendationField.CREATED_AT.value, pymongo.DESCENDING)]
        if recommendation_sort is not None:
            query_sort = recommendation_sort
        if excluded_ids is None:
            excluded_ids = []

        operation_start_time = datetime.now()
        try:
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
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to get recommendations page. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=recommendation_filter)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                data=response_dict,
                                description='Get campaigns with recommendations page',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=recommendation_filter)

        return response_dict

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def set_recommendation_statuses_by_structure_id(self, structure_id, status):
        now = datetime.now()
        operation_start_time = datetime.now()
        query_filter = {RecommendationField.STRUCTURE_ID.value: structure_id,
                        RecommendationField.STATUS.value: RecommendationStatusEnum.ACTIVE.value}

        query = {MongoOperator.SET.value: {
                    RecommendationField.STATUS.value: status,
                    RecommendationField.APPLICATION_DATE.value: now,
                    RecommendationField.APPLIED_BY.value: 'Dexter'}}
        try:
            self.collection.update_many(query_filter, query)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to get recommendations page. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                query_filter=query_filter)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Get campaigns with recommendations page',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query)

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def set_recommendation_status(self, recommendation_id: str, status: str):
        recommendation_object_id = ObjectId(recommendation_id)
        now = datetime.now()
        operation_start_time = datetime.now()
        query_filter = {RecommendationField.OBJECT_ID.value: recommendation_object_id}
        query = {MongoOperator.SET.value: { RecommendationField.STATUS.value: status,
                                            RecommendationField.APPLICATION_DATE.value: now,
                                            RecommendationField.APPLIED_BY.value: 'Dexter'}}
        try:
            self.collection.update_one(query_filter, query)

            recommendation = (self.collection.find_one({RecommendationField.OBJECT_ID.value: recommendation_object_id})).__dict__
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to set recommendation status. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                query_filter=query_filter)
            raise e
        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Set recommendation status',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                query_filter=query_filter)

        return recommendation

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_action_history(self, structure_id: str):
        query = {RecommendationField.STRUCTURE_ID.value: structure_id,
                 RecommendationField.STATUS.value: {MongoOperator.IN.value: [RecommendationStatusEnum.APPLIED.value,
                                                    RecommendationStatusEnum.DISMISSED.value]}}
        projection = {RecommendationField.APPLICATION_DETAILS.value: False}
        operation_start_time = datetime.now()
        try:
            cursor = self.collection.find(query, projection).sort(RecommendationField.APPLICATION_DATE.value, pymongo.DESCENDING)
            action_histories_as_dict_list = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in
                                             list(cursor)]
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to set recommendation status. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                projection=projection)
            raise e
        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Set recommendation status',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query,
                                projection=projection)
        return action_histories_as_dict_list

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
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
        operation_start_time = datetime.now()
        try:
            count = self.get_count_by_filter(query_filter)
            response = self.collection.find(query_filter, projection)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to get recommendations. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query_filter,
                                projection=projection)
            raise e
        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Get recommendations',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=query_filter,
                                projection=projection)
        return response, count

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
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
        operation_start_time = datetime.now()
        try:
            cursor = self.collection.aggregate(aggregation)
            counts = list(cursor)

            for reco_type in RecommendationType:
                type_count = 0
                for count in counts:
                    if count[MongoOperator.GROUP_KEY.value] == reco_type.value:
                        type_count = count['count']

                counts_by_type[reco_type.value] = type_count
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to counts by type. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=aggregation)
            raise e

        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Get recommendations',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=aggregation)

        return counts_by_type

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
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

        operation_start_time = datetime.now()
        try:
            cursor = self.collection.aggregate(aggregation)
            counts = list(cursor)

            for metric in RecommendationCategory:
                metric_count = 0
                for count in counts:
                    if count[MongoOperator.GROUP_KEY.value] == metric.value:
                        metric_count = count['count']

                counts_by_category[metric.value] = metric_count

        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to counts by category. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=aggregation)
            raise e
        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Get counts by category',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=aggregation)
        return counts_by_category

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_counts(self, recommendation_filter):
        types = self.get_counts_by_type(recommendation_filter)
        metrics = self.get_counts_by_category(recommendation_filter)
        types.update(metrics)
        return types

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def get_count_by_filter(self, recommendation_filter=None):
        count_filter = {}
        if recommendation_filter is not None:
            count_filter = recommendation_filter
        operation_start_time = datetime.now()
        try:
            count = self.collection.count_documents(count_filter)
        except Exception as e:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                description=f'Failed to counts by filter. Reason: {str(e)}',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=count_filter)
            raise e
        if self._logger.level == LoggingLevelEnum.DEBUG.value:
            operation_end_time = datetime.now()
            duration = (operation_end_time - operation_start_time).total_seconds()
            log_operation_mongo(logger=self._logger,
                                log_level=LoggerMessageTypeEnum.EXEC_DETAILS,
                                description='Get counts by filter',
                                timestamp=operation_end_time,
                                duration=duration,
                                query=count_filter)
        return count
