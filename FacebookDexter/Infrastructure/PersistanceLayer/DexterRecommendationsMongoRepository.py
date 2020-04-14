from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase


class DexterRecommendationsMongoRepository(MongoRepositoryBase):

    def save_recommendations(self, recommendations):
        self._database = self._client[self._config.recommendations_database_name]
        self.set_collection(self._config.recommendations_collection_name)

        self.add_many(recommendations)
