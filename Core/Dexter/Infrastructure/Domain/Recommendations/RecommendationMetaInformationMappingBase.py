import typing

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField


class RecommendationMetaInformationMappingBase():
    _mapping = {
        # implement this in your classes which inherit this one
    }

    def __init__(self, level: LevelEnum = None):
        self.__level = level
        if not self._mapping:
            raise NotImplementedError

    def apply_map(self, structure_meta_information: typing.Dict) -> typing.Dict:
        meta_information = {key: structure_meta_information.get(value) for key, value in
                            self._mapping[self.__level].items()}
        meta_information[RecommendationField.AD_ACCOUNT_ID.value] = self._map_account_id(
            meta_information[RecommendationField.AD_ACCOUNT_ID.value])
        return meta_information

    @staticmethod
    def _map_account_id(account_id: typing.AnyStr = None) -> typing.AnyStr:
        return "act_" + account_id
