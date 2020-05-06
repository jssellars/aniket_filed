import itertools
from functools import reduce

import pandas as pd

from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from GoogleTuring.Infrastructure.Domain.Enums.Breakdown import BREAKDOWN_TO_FIELD, DEFAULT_GEO_BREAKDOWN
from GoogleTuring.Infrastructure.PersistanceLayer.MongoIdToNameCache import MongoIdToNameCache


class GoogleTuringInsightsMongoRepository(MongoRepositoryBase):
    def __init__(self, client=None, database_name=None, collection_name=None, config=None, location_collection_name=None):
        super().__init__(client=client, database_name=database_name, collection_name=collection_name, config=config)
        self.__location_collection_name = location_collection_name
        self.collection = self.__location_collection_name
        location_data = self.get_all()
        MongoIdToNameCache.id_to_name_cache = {entry['id']: entry['locationName'] for entry in location_data}

    def __insert_locations_into_db(self, unknown_ids, adwords_client):
        self.collection = self.__location_collection_name
        location_criterion_service = adwords_client.get_location_criterion_service()

        selector = {
            'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
                       'ParentLocations', 'Reach', 'TargetingStatus'],
            'predicates': [{
                'field': 'Id',
                'operator': 'IN',
                'values': unknown_ids
            }]
        }

        location_criteria = location_criterion_service.get(selector)

        locations_to_be_added = []
        collection_keys = ['id', 'locationName']

        for location in location_criteria:
            entry = {key: location['location'][key] for key in collection_keys}
            locations_to_be_added.append(entry)

        self.add_many(locations_to_be_added)
        MongoIdToNameCache.update_id_to_location_cache(locations_to_be_added)

    def insert_insights_into_db(self, collection_name, df, fields, compound_fields, start_date, end_date):
        def custom_concat(series):
            return reduce(lambda x, y: x + " " + y if x is not None and y is not None else None, series)

        self.collection = collection_name

        extra_fields_dict = {compound_field.name: compound_field.required_fields for compound_field in compound_fields}
        extra_fields = list(itertools.chain(*extra_fields_dict.values()))

        df = df.where(df != ' --', None)
        df = df.where(pd.notnull(df), None)

        for field in fields:
            if field.conversion_function is not None:
                df[field.name] = df[field.name].apply(field.conversion_function)

        for field_name, corresponding_fields in extra_fields_dict.items():
            corresponding_field_names = list(map(lambda x: x.name, corresponding_fields))
            df[field_name] = df[corresponding_field_names].agg(custom_concat, axis=1)

        df['start_date'] = start_date
        df['end_date'] = end_date

        extra_field_names = list(map(lambda x: x.name, extra_fields))
        df = df.drop(columns=extra_field_names)
        self.add_many(df.to_dict('r'))

    def update_locations_if_needed(self, df, breakdown, client):
        resulting_ids = []
        default_location_field = BREAKDOWN_TO_FIELD[DEFAULT_GEO_BREAKDOWN]
        breakdown_location_field = BREAKDOWN_TO_FIELD[breakdown]

        default_location_ids = list(df[default_location_field.name].unique())
        breakdown_location_ids = list(df[breakdown_location_field.name].unique())

        location_ids_list = [default_location_ids] + [breakdown_location_ids]
        for location_ids in location_ids_list:
            if ' --' in location_ids:
                location_ids.remove(' --')
            resulting_ids.extend(location_ids)

        resulting_ids = list(map(lambda x: int(x), resulting_ids))

        stored_ids = MongoIdToNameCache.id_to_name_cache.keys()
        unknown_ids = list(set(resulting_ids) - set(stored_ids))

        if len(unknown_ids) != 0:
            self.__insert_locations_into_db(unknown_ids, client)
