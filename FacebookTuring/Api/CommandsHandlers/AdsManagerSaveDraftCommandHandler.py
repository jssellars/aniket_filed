from FacebookTuring.Api.startup import config
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerSaveDraftCommandHandler:

    @classmethod
    def handle(cls, command, level, facebook_id):
        try:
            repository = TuringMongoRepository(config=config.mongo,
                                               database_name=config.mongo.structures_database_name,
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
