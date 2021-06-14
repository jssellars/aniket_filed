"""
Base Class for Labs Hidden Interests Command Handlers.

"""
# Standard Imports.
from abc import ABC, abstractmethod
from typing import Dict, AnyStr


class LabsHiddenInterestsCommandHandlersBase(ABC):

    @abstractmethod
    def handle(self, query_json: Dict, business_owner_id: AnyStr):
        pass

    @staticmethod
    def map_query(self, query_json: Dict):
        pass
