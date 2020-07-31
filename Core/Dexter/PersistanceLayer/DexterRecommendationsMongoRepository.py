import typing
from datetime import datetime, timedelta

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Tools.Misc.Constants import DEFAULT_DATETIME_ISO
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum


class DexterRecommendationsMongoRepository(MongoRepositoryBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __get_existing_recommendations_ids(self,
                                           recommendation_ids: typing.List[typing.AnyStr] = None,
                                           date: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        query = {
            MongoOperator.AND.value: [
                {
                    RecommendationField.RECOMMENDATION_ID.value: {
                        MongoOperator.IN.value: recommendation_ids
                    }
                },
                {
                    RecommendationField.CREATED_AT.value: {
                        MongoOperator.GREATERTHANEQUAL.value: date
                    }
                },
                {
                    RecommendationField.STATUS.value: {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
                },
            ]
        }

        # build mongo projection
        projection = {
            RecommendationField.OBJECT_ID.value: MongoProjectionState.OFF.value,
            RecommendationField.RECOMMENDATION_ID.value: MongoProjectionState.ON.value
        }

        results = self.get(query, projection)

        return [result[RecommendationField.RECOMMENDATION_ID.value] for result in results]

    def __get_old_recommendations(self, date: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        query = {
            MongoOperator.AND.value: [
                {
                    RecommendationField.CREATED_AT.value: {
                        MongoOperator.LESSTHANEQUAL.value: date
                    }
                },
                {
                    RecommendationField.STATUS.value: {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
                },
            ]
        }

        # build mongo projection
        projection = {
            RecommendationField.OBJECT_ID.value: MongoProjectionState.OFF.value,
            RecommendationField.RECOMMENDATION_ID.value: MongoProjectionState.ON.value
        }

        results = self.get(query, projection)

        return [result['recommendation_id'] for result in results]

    def deprecate_recommendations(self, recommendation_ids: typing.List[typing.AnyStr]) -> typing.NoReturn:
        query_filter = {
            MongoOperator.AND.value: [
                {
                    RecommendationField.RECOMMENDATION_ID.value: {
                        MongoOperator.IN.value: recommendation_ids
                    }
                },
                {
                    RecommendationField.STATUS.value: {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
                }
            ]
        }
        query = {
            MongoOperator.SET.value: {
                RecommendationField.STATUS.value: RecommendationStatusEnum.DEPRECATED.value,
                RecommendationField.LAST_UPDATED_AT.value: datetime.now()
            }
        }
        self.update_many(query_filter, query)

    def get_active_recommendations(self) -> typing.List:
        query_filter = {
                    RecommendationField.STATUS.value: {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
        }
        results = self.get(query_filter)

        return results

    def save_recommendations(self, recommendations: typing.List[typing.Any],
                             time_interval: int = None) -> typing.NoReturn:
        self._database = self._client[self._config.recommendations_database_name]
        self.set_collection(self._config.recommendations_collection_name)

        date = (datetime.now() - timedelta(days=time_interval)).strftime(DEFAULT_DATETIME_ISO)

        # get existing recommendations
        recommendation_ids = [recommendation[RecommendationField.RECOMMENDATION_ID.value] for recommendation in recommendations]
        existing_recommendations = self.__get_existing_recommendations_ids(recommendation_ids, date)

        # deprecate recommendations
        old_recommendations = self.__get_old_recommendations(date)
        self.deprecate_recommendations(old_recommendations)

        # add new recommendations
        new_recommendations_ids = set(recommendation_ids) - set(existing_recommendations)
        new_recommendations_ids = list(new_recommendations_ids - set(old_recommendations))
        new_recommendations = [recommendation
                               for recommendation in recommendations
                               if recommendation[RecommendationField.RECOMMENDATION_ID.value] in new_recommendations_ids]
        self.add_many(new_recommendations)
