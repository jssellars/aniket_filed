from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Core.Tools.MongoRepository.graceful_auto_reconnect import graceful_auto_reconnect
from GoogleTuring.Infrastructure.Domain.Structures.StructureStatus import StructureStatus


class GoogleTuringStructuresMongoRepository(MongoRepositoryBase):

    def update_removed_structures(self, deleted_customer_ids):
        if deleted_customer_ids:
            collection_names = self.database.list_collection_names()
            for collection_name in collection_names:
                self.collection = collection_name
                self.change_status_many(ids=deleted_customer_ids, new_status=StructureStatus.REMOVED.value, id_key="account_id")

    def add_structures(self, structure_mapping):
        processed_entries = structure_mapping.process()
        id_key = structure_mapping.get_structure_id()
        structure_ids = list(map(lambda x: x[id_key], processed_entries))

        query = {
            MongoOperator.AND.value: [{
                id_key: {
                    MongoOperator.IN.value: structure_ids
                },
                "status": {MongoOperator.IN.value: [StructureStatus.ENABLED.value, StructureStatus.PAUSED.value]}
            }]
        }

        existing_structures = self.get(query)
        existing_ids = list(map(lambda x: x[id_key], existing_structures))

        removed_structures_ids = list(set(existing_ids) - set(structure_ids))
        if removed_structures_ids:
            self.change_status_many(ids=removed_structures_ids, new_status=StructureStatus.REMOVED.value, id_key=id_key)

        new_structures_ids = list(set(structure_ids) - set(existing_ids))
        if new_structures_ids:
            new_structures = list(filter(lambda x: x[id_key] in new_structures_ids, processed_entries))
            self.add_many(new_structures)

        common_structures_ids = list(set(structure_ids) & set(existing_ids))
        common_structures = list(filter(lambda x: x[id_key] in common_structures_ids, processed_entries))

        if common_structures_ids:
            self.change_status_many(ids=common_structures_ids, new_status=StructureStatus.DEPRECATED.value, id_key=id_key)
            self.add_many(common_structures)
