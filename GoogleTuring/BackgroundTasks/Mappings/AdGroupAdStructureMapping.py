from datetime import datetime

from bson import BSON
from zeep import helpers

from GoogleTuring.BackgroundTasks.Mappings.StructureMapping import StructureMapping
from GoogleTuring.Infrastructure.Domain.Structures.StructureStatus import GOOGLE_STATUS_MAPPING
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType, LEVEL_TO_ID


class AdGroupAdStructureMapping(StructureMapping):
    _PAGE_SIZE = 3000

    def __init__(self, business_owner_id, account_id, ad_group_details, service, structure_fields, entries=None):
        super().__init__(business_owner_id, account_id, service, structure_fields, entries)
        self.__ad_group_details = ad_group_details

    def _set_structure_id(self):
        self._structure_id = LEVEL_TO_ID[StructureType.AD]

    def process(self):
        def build_ad_name():
            ad_entry = entry['ad']
            name_fields = ['headlinePart1', 'headlinePart2', 'headlinePart3']
            name_parts = list(map(lambda x: ad_entry[x] if x in ad_entry else None, name_fields))
            name_parts = list(filter(lambda x: x is not None, name_parts))
            if name_parts:
                ad_name = ' '.join(name_parts)
                return ad_name
            return None

        processed_entries = []

        for entry in self._entries:
            processed_entry = dict(business_owner_id=self._business_owner_id, account_id=self._account_id)
            processed_entry[self._structure_id] = str(entry['ad']['id'])
            ad_group_id = str(entry['adGroupId'])
            processed_entry[LEVEL_TO_ID[StructureType.AD_GROUP]] = ad_group_id

            if ad_group_id in self.__ad_group_details:
                ad_group_info = self.__ad_group_details[ad_group_id]
                processed_entry['adgroup_name'] = ad_group_info['adgroup_name']
                processed_entry['campaign_name'] = ad_group_info['campaign_name']
                processed_entry[LEVEL_TO_ID[StructureType.CAMPAIGN]] = ad_group_info['campaign_id']
            else:
                processed_entry['adgroup_name'] = None
                processed_entry['campaign_name'] = None
                processed_entry['campaign_id'] = None

            processed_entry['ad_name'] = build_ad_name()
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
