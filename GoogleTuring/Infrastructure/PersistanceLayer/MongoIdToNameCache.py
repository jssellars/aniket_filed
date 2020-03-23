from dataclasses import dataclass
from typing import Dict


@dataclass
class MongoIdToNameCache:
    id_to_name_cache: Dict = None

    @staticmethod
    def update_id_to_location_cache(location_data):
        for entry in location_data:
            MongoIdToNameCache.id_to_name_cache[entry['id']] = entry['locationName']
