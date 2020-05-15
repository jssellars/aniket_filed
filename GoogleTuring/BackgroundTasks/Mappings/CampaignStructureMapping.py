from datetime import datetime

from bson import BSON
from zeep import helpers

from GoogleTuring.BackgroundTasks.Mappings.StructureMapping import StructureMapping
from GoogleTuring.Infrastructure.Domain.Structures.StructureStatus import GOOGLE_STATUS_MAPPING


class CampaignStructureMapping(StructureMapping):
    _PAGE_SIZE = 200

    def __init__(self, business_owner_id, account_id, service, structure_fields, entries=None):
        super().__init__(business_owner_id, account_id, service, structure_fields, entries)

    def _set_structure_id(self):
        self._structure_id = 'campaign_id'

    def process(self):
        processed_entries = []

        for entry in self._entries:
            processed_entry = dict(business_owner_id=self._business_owner_id, account_id=self._account_id)
            processed_entry['campaign_name'] = entry['name']
            processed_entry[self._structure_id] = entry['id']
            processed_entry['last_updated_at'] = datetime.now()
            processed_entry['actions'] = None
            processed_entry['status'] = GOOGLE_STATUS_MAPPING[entry['status']]

            processed_entry['details'] = entry
            processed_entry = helpers.serialize_object(processed_entry)
            processed_entry['details'] = BSON.encode(processed_entry['details'])

            processed_entries.append(processed_entry)

        return processed_entries
