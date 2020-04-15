from datetime import datetime

from bson import BSON
from googleads import adwords
from zeep import helpers

from GoogleTuring.BackgroundTasks.Mappings.StructureMapping import StructureMapping
from GoogleTuring.Infrastructure.Domain.Structures.StructureStatus import GOOGLE_STATUS_MAPPING


class AdGroupKeywordsMapping(StructureMapping):
    _PAGE_SIZE = 2000

    def __init__(self, business_owner_id, account_id, service, structure_fields, ad_group_details):
        super().__init__(business_owner_id, account_id, service, structure_fields)
        self.__ad_group_details = ad_group_details

    def _set_structure_id(self):
        self._structure_id = 'keywords_id'

    def process(self):
        processed_entries = []

        for entry in self._entries:
            processed_entry = dict(business_owner_id=self._business_owner_id, account_id=self._account_id)
            ad_group_id = entry['adGroupId']
            processed_entry['ad_group_id'] = ad_group_id

            if ad_group_id in self.__ad_group_details:
                ad_group_info = self.__ad_group_details[ad_group_id]
                processed_entry['ad_group_name'] = ad_group_info['ad_group_name']
                processed_entry['campaign_name'] = ad_group_info['campaign_name']
                processed_entry['campaign_id'] = ad_group_info['campaign_id']
            else:
                processed_entry['ad_group_name'] = None
                processed_entry['campaign_name'] = None
                processed_entry['campaign_id'] = None

            processed_entry[self._structure_id] = entry['criterion']['id']
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
            # TODO: log error
            print("Exception " + e.__str__() + " has occurred")

        return entries
