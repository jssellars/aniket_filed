import json
import datetime

from Packages.MongoRepository.MongoRepositoryBase import MongoRepositoryBase


class MongoRepositoryRecommender(MongoRepositoryBase):
    def __init__(self, client, database_name, collection_name=None):
        super().__init__(client=client, database_name=database_name, collection_name=collection_name)

    def send_recommendations(self, recommendations):
        for i, recommendation in enumerate(recommendations):
            saving_recommendation = recommendation
            saving_recommendation.createdAt = datetime.datetime.now()
            saving_recommendation_dict = saving_recommendation.__dict__
            saving_recommendation_dict['applicationDetails'] = json.dumps(recommendation.applicationDetails)
            self.add_one(saving_recommendation_dict)

            print(f"Sent recommendation:", saving_recommendation_dict)
