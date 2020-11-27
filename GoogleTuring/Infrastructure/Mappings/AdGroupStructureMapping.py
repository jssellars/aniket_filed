from copy import deepcopy
from datetime import datetime

from bson import BSON
from googleads import adwords
from zeep import helpers

from Core.logging_legacy import log_operation_mongo
from GoogleTuring.Infrastructure.Domain.StructureStatusEnum import GOOGLE_STATUS_MAPPING
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import LEVEL_TO_ID, StructureType
from GoogleTuring.Infrastructure.Mappings.StructureMapping import StructureMapping


import logging

logger_native = logging.getLogger(__name__)


class AdGroupStructureMapping(StructureMapping):
    _PAGE_SIZE = 1000

    def __init__(self, business_owner_id, account_id, service, structure_fields, criterion_service, criterion_fields,
                 entries=None):
        super().__init__(business_owner_id, account_id, service, structure_fields, entries)
        self.__ad_group_details = {}
        self.__criterion_service = criterion_service
        self.__criterion_fields = criterion_fields

    def _set_structure_id(self):
        self._structure_id = LEVEL_TO_ID[StructureType.AD_GROUP]

    def process(self):
        processed_entries = []
        ad_group_id_to_entry = {}
        for entry in self._entries:
            processed_entry = dict(business_owner_id=self._business_owner_id, ad_account_id=self._account_id)
            processed_entry['adgroup_name'] = entry['name']
            ad_group_id = str(entry['id'])
            processed_entry[self._structure_id] = ad_group_id

            processed_entry['campaign_name'] = entry['campaignName']
            processed_entry['campaign_id'] = str(entry['campaignId'])

            processed_entry['last_updated_at'] = datetime.now()
            processed_entry['actions'] = None
            processed_entry['status'] = GOOGLE_STATUS_MAPPING[entry['status']]

            for key, value in processed_entry.items():
                entry[key] = value

            processed_entry['details'] = entry

            self.__ad_group_details[processed_entry[self._structure_id]] = {
                'campaign_id': processed_entry['campaign_id'],
                'campaign_name': processed_entry['campaign_name'],
                'adgroup_name': processed_entry['adgroup_name']}

            ad_group_id_to_entry[ad_group_id] = processed_entry

        criteria_entries = self.__get_criteria_for_ad_groups()

        for ad_group_id, entry in ad_group_id_to_entry.items():
            if int(ad_group_id) in criteria_entries:
                entry['details']['criteria'] = criteria_entries[int(ad_group_id)]
            else:
                entry['details']['criteria'] = None

            serialized_entry = helpers.serialize_object(entry)
            serialized_entry['details'] = BSON.encode(serialized_entry['details'])
            processed_entries.append(serialized_entry)

        return processed_entries

    def get_ad_group_details(self):
        return deepcopy(self.__ad_group_details)

    def clear_ad_group_details(self):
        self.__ad_group_details = {}

    def __get_criteria_for_ad_groups(self):
        query = (adwords.ServiceQueryBuilder()
                 .Select(*self.__criterion_fields)
                 .Limit(0, self._PAGE_SIZE)
                 .Build())

        entries = {}

        try:
            for page in query.Pager(self.__criterion_service):
                if 'entries' in page:
                    for entry in page['entries']:
                        ad_group_id = entry['adGroupId']
                        if ad_group_id in entries:
                            entries[ad_group_id] += [entry]
                        else:
                            entries[ad_group_id] = [entry]
        except Exception as e:
            log_operation_mongo(logger=self.logger,
                                log_level=logging.ERROR,
                                query=query,
                                description=f'Failed to get criteria for AdGroups. Reason: {e}'
                                )
            print("Exception " + e.__str__() + " has occurred")

        return entries
