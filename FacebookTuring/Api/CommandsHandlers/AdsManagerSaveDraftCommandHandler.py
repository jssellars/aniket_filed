from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerSaveDraftCommandHandler:

    @classmethod
    def handle(cls, command, level, facebook_id):
        try:
            repository = TuringMongoRepository(config=startup.mongo_config,
                                               database_name=startup.mongo_config['structures_database_name'],
                                               collection_name=level)

            repository.save_structure_draft(Level(level), facebook_id, command.details)
            repository.close()
        except Exception as e:
            raise e
