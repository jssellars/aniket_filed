from datetime import datetime

from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Core.Tools.MongoRepository.MongoRepositoryStatusBase import MongoRepositoryStatusBase
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureMapping


class TuringMongoRepository(MongoRepositoryBase):

    def __init__(self, *args, **kwargs):
        super(TuringMongoRepository, self).__init__(*args, **kwargs)

    def get_existing_data_by_ids(self, id_key="facebook_id", facebook_ids=None):
        query = {
            id_key: {
                MongoOperator.IN.value: facebook_ids
            }
        }
        try:
            results = self.collection.find(query)
        except Exception as e:
            raise e

        return results

    def add_structures(self, structures=None, level=None, id_key="facebook_id"):
        structure_ids = [getattr(structure, id_key) for structure in structures]

        # find existing structures
        query = {
            MongoOperator.AND.value: [{
                id_key: {
                    MongoOperator.IN.value: structure_ids
                },
                "status": {
                    MongoOperator.EQUALS.value: MongoRepositoryStatusBase.ACTIVE.value
                }
            }]
        }

        mapping = StructureMapping.get(level)

        existing_structures = self.get(query)
        existing_matching_structures = [mapping.load(entry) for entry in existing_structures]

        # intersect existing with response ids
        existing_ids = [getattr(structure, id_key) for structure in existing_matching_structures]

        # for all ids in existing and not in response, mark them as removed
        removed_structures_ids = list(set(existing_ids) - set(structure_ids))
        if removed_structures_ids:
            self.change_status_many(removed_structures_ids, MongoRepositoryStatusBase.REMOVED.value)

        # for all ids in response and not in response, add them as new
        new_structures_ids = list(set(structure_ids) - set(existing_ids))
        if new_structures_ids:
            new_structures = [structure for structure in structures if getattr(structure, id_key) in new_structures_ids]
            self.add_many(new_structures)

        # for all ids in response and existing, add structures + update_one status for existing to Deprecated
        common_structures_ids = list(set(structure_ids) & set(existing_ids))
        common_structures = [structure for structure in structures if getattr(structure, id_key) in common_structures_ids]

        for structure in common_structures:
            # TODO: get a better way to update_one only the ones that have updated_time on FB > last_updated_time on Mongo
            is_updated = self.change_status_to_match_facebook(getattr(structure, id_key),
                                                              structure.details.updated_time,
                                                              MongoRepositoryStatusBase.DEPRECATED.value)
            if is_updated:
                structure.last_updated_at = datetime.now()
                self.add_one(structure)

    def discard_structure_draft(self, facebook_id, id_key="facebook_id"):
        query_filter = {
            id_key: {
                MongoOperator.EQUALS.value: facebook_id
            }
        }

        query = {
            MongoOperator.SET.value: {
                "actions": None,
                "last_updated_at": datetime.now()
            }
        }

        return self.update_one(query_filter, query)

    def save_structure_draft(self, facebook_id, details, id_key="facebook_id"):
        query_filter = {
            id_key: {
                MongoOperator.EQUALS.value: facebook_id
            }
        }

        query = {
            MongoOperator.SET.value: {
                "actions": details,
                "last_updated_at": datetime.now()
            }
        }

        return self.update_one(query_filter, query)
