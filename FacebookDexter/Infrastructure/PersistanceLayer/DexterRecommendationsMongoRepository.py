import typing
from datetime import datetime, timedelta

from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase, MongoProjectionState
from FacebookDexter.Infrastructure.Constants import DEFAULT_DATETIME_ISO
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum


class DexterRecommendationsMongoRepository(MongoRepositoryBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __get_existing_recommendations_ids(self,
                                           recommendation_ids: typing.List[typing.AnyStr] = None,
                                           date: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        query = {
            MongoOperator.AND.value: [
                {
                    'recommendation_id': {
                        MongoOperator.IN.value: recommendation_ids
                    }
                },
                {
                    'created_at': {
                        MongoOperator.GREATERTHANEQUAL.value: date
                    }
                },
                {
                    'status': {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
                },
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            "recommendation_id": MongoProjectionState.ON.value
        }

        results = self.get(query, projection)

        return [result['recommendation_id'] for result in results]

    def __get_old_recommendations(self, date: typing.AnyStr = None) -> typing.List[typing.AnyStr]:
        query = {
            MongoOperator.AND.value: [
                {
                    'created_at': {
                        MongoOperator.LESSTHANEQUAL.value: date
                    }
                },
                {
                    'status': {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
                },
            ]
        }

        # build mongo projection
        projection = {
            "_id": MongoProjectionState.OFF.value,
            "recommendation_id": MongoProjectionState.ON.value
        }

        results = self.get(query, projection)

        return [result['recommendation_id'] for result in results]

    def deprecate_recommendations(self, recommendation_ids: typing.List[typing.AnyStr]) -> typing.NoReturn:
        query_filter = {
            MongoOperator.AND.value: [
                {
                    'recommendation_id': {
                        MongoOperator.IN.value: recommendation_ids
                    }
                },
                {
                    'status': {
                        MongoOperator.EQUALS.value: RecommendationStatusEnum.ACTIVE.value
                    }
                }
            ]
        }
        query = {
            MongoOperator.SET.value: {
                'status': RecommendationStatusEnum.DEPRECATED.value,
                'last_updated_at': datetime.now()
            }
        }
        self.update_many(query_filter, query)

    def get_active_recommendations(self) -> typing.List:
        query_filter = {
                    'status': {
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
        recommendation_ids = [recommendation['recommendation_id'] for recommendation in recommendations]
        existing_recommendations = self.__get_existing_recommendations_ids(recommendation_ids, date)

        # deprecate recommendations
        old_recommendations = self.__get_old_recommendations(date)
        self.deprecate_recommendations(old_recommendations)

        # add new recommendations
        new_recommendations_ids = set(recommendation_ids) - set(existing_recommendations)
        new_recommendations_ids = list(new_recommendations_ids - set(old_recommendations))
        new_recommendations = [recommendation
                               for recommendation in recommendations
                               if recommendation['recommendation_id'] in new_recommendations_ids]
        self.add_many(new_recommendations)
