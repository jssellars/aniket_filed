from datetime import datetime

from bson import BSON
from zeep import helpers

from GoogleTuring.BackgroundTasks.Mappings.StructureMapping import StructureMapping
from GoogleTuring.Infrastructure.Domain.StructureStatusEnum import GOOGLE_STATUS_MAPPING
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import LEVEL_TO_ID, StructureType


class CampaignStructureMapping(StructureMapping):
    _PAGE_SIZE = 200

    def __init__(self, business_owner_id, account_id, service, structure_fields, entries=None):
        super().__init__(business_owner_id, account_id, service, structure_fields, entries)

    def _set_structure_id(self):
        self._structure_id = LEVEL_TO_ID[StructureType.CAMPAIGN]

    def process(self):
        processed_entries = []

        for entry in self._entries:
            processed_entry = dict(business_owner_id=self._business_owner_id, ad_account_id=self._account_id)
            processed_entry['campaign_name'] = entry['name']
            processed_entry[self._structure_id] = str(entry['id'])
            processed_entry['last_updated_at'] = datetime.now()
            processed_entry['actions'] = None
            processed_entry['status'] = GOOGLE_STATUS_MAPPING[entry['status']]

            for key, value in processed_entry.items():
                entry[key] = value

            processed_entry['details'] = entry
            processed_entry = helpers.serialize_object(processed_entry)
            processed_entry['details'] = BSON.encode(processed_entry['details'])

            processed_entries.append(processed_entry)

        return processed_entries
