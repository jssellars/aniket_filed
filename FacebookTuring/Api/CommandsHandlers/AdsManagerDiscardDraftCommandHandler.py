from FacebookTuring.Api.startup import config, fixtures
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDiscardDraftCommandHandler:

    @classmethod
    def handle(cls, level, facebook_id):
        try:
            repository = TuringMongoRepository(config=config.mongo,
                                               database_name=config.mongo.structures_database_name,
                                               collection_name=level)
            repository.discard_structure_draft(Level(level), facebook_id)
        except Exception as e:
            raise e
