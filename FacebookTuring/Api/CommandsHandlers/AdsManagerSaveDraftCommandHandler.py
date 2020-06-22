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
            structure = repository.get_structure_details(Level(level), facebook_id)
            draft = structure.get('details')
            if draft:
                draft.update(command.details)
            else:
                draft = command.details
            repository.save_structure_draft(Level(level), facebook_id, draft)
        except Exception as e:
            raise e
