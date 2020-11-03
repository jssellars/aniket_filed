from datetime import datetime

from bson import BSON
from googleads import adwords
from zeep import helpers

from Core.Tools.Logger.Helpers import log_operation_mongo
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum
from GoogleTuring.Infrastructure.Domain.StructureStatusEnum import GOOGLE_STATUS_MAPPING
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import LEVEL_TO_ID, StructureType
from GoogleTuring.Infrastructure.Mappings.StructureMapping import StructureMapping


class AdGroupKeywordsMapping(StructureMapping):
    _PAGE_SIZE = 2000

    def __init__(self, business_owner_id, account_id, service, structure_fields, ad_group_details, entries=None, **kwargs):
        super().__init__(business_owner_id, account_id, service, structure_fields, entries, **kwargs)
        self.__ad_group_details = ad_group_details

    def _set_structure_id(self):
        self._structure_id = LEVEL_TO_ID[StructureType.AD_GROUP_KEYWORDS]

    def process(self):
        processed_entries = []

        for entry in self._entries:
            processed_entry = dict(business_owner_id=self._business_owner_id, ad_account_id=self._account_id)
            ad_group_id = str(entry['adGroupId'])
            processed_entry[LEVEL_TO_ID[StructureType.AD_GROUP]] = ad_group_id

            if ad_group_id in self.__ad_group_details:
                ad_group_info = self.__ad_group_details[ad_group_id]
                processed_entry['adgroup_name'] = ad_group_info['adgroup_name']
                processed_entry['campaign_name'] = ad_group_info['campaign_name']
                processed_entry['campaign_id'] = ad_group_info['campaign_id']
            else:
                processed_entry['adgroup_name'] = None
                processed_entry['campaign_name'] = None
                processed_entry['campaign_id'] = None

            processed_entry[self._structure_id] = str(entry['criterion']['id'])
            processed_entry['keywords'] = entry['criterion']['text']
            processed_entry['match_type'] = entry['criterion']['matchType']
            processed_entry['last_updated_at'] = datetime.now()
            processed_entry['actions'] = None

            if 'userStatus' in entry:
                # for biddable criteria
                processed_entry['status'] = GOOGLE_STATUS_MAPPING[entry['userStatus']]
            else:
                # for negative criteria
                processed_entry['status'] = GOOGLE_STATUS_MAPPING['ENABLED']

            for key, value in processed_entry.items():
                entry[key] = value

            processed_entry['details'] = entry

            processed_entry = helpers.serialize_object(processed_entry)
            processed_entry['details'] = BSON.encode(processed_entry['details'])
            processed_entries.append(processed_entry)

        return processed_entries

    def _get_structure_entries(self):
        query = (adwords.ServiceQueryBuilder()
                 .Select(*self._structure_fields)
                 .Where('Status').In('ENABLED', 'PAUSED')
                 .Where('CriteriaType').EqualTo('KEYWORD')
                 .Limit(0, self._PAGE_SIZE)
                 .Build())

        entries = []
        try:
            for page in query.Pager(self._service):
                if 'entries' in page:
                    entries.extend(page['entries'])
        except Exception as e:
            log_operation_mongo(logger=self.logger,
                                log_level=LoggerMessageTypeEnum.ERROR,
                                query=query,
                                description=f'Failed to get Adgroup structure entries. Reason: {e}'
                                )

        return entries
