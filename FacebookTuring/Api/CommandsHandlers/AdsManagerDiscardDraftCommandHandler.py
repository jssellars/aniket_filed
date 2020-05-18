from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDiscardDraftCommandHandler:

    @classmethod
    def handle(cls, level, facebook_id):
        try:
            repository = TuringMongoRepository(config=startup.mongo_config,
                                               database_name=startup.mongo_config['structures_database_name'],
                                               collection_name=level)
            repository.discard_structure_draft(Level(level), facebook_id)
            repository.close()
        except Exception as e:
            raise e
