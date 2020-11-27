from googleads import adwords

from Core.logging_legacy import log_operation_mongo


import logging

logger_native = logging.getLogger(__name__)


class StructureMapping:
    _PAGE_SIZE = 100

    def __init__(self, business_owner_id, account_id, service, structure_fields, entries, logger=None):
        self._business_owner_id = business_owner_id
        self._account_id = account_id
        self._service = service
        self._structure_fields = structure_fields
        self.logger = logger
        if not entries:
            self._entries = self._get_structure_entries()
        else:
            self._entries = entries

        self._structure_id = None
        self._set_structure_id()

    def _set_structure_id(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def get_structure_id(self):
        return self._structure_id

    def _get_structure_entries(self):
        query = (adwords.ServiceQueryBuilder()
                 .Select(*self._structure_fields)
                 .Where('Status').In('ENABLED', 'PAUSED')
                 .Limit(0, self._PAGE_SIZE)
                 .Build())

        entries = []
        try:
            for page in query.Pager(self._service):
                if 'entries' in page:
                    entries.extend(page['entries'])
        except Exception as e:
            log_operation_mongo(logger=self.logger,
                                log_level=logging.ERROR,
                                query=query,
                                description=f'Failed to get structure entries. Reason: {e}')

        return entries
