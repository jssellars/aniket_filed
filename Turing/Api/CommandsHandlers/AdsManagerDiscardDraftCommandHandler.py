from Turing.Api.Startup import startup
from Turing.Infrastructure.Mappings.LevelMapping import LevelToFacebookIdKeyMapping
from Turing.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class AdsManagerDiscardDraftCommandHandler:

    @classmethod
    def handle(cls, level, facebook_id):
        mongo_repository = TuringMongoRepository(config=startup.mongo_config,
                                                 database_name=startup.mongo_config['structures_database_name'],
                                                 collection_name=level)

        return mongo_repository.discard_structure_draft(facebook_id, id_key=LevelToFacebookIdKeyMapping.get_by_name(level))
