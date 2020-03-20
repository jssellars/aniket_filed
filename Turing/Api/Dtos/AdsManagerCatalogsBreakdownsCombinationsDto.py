import Turing.Api.Catalogs.Breakdowns.BreakdownsCombinations
from Core.Tools.Misc.ObjectSerializers import object_to_json


class AdsManagerCatalogsBreakdownsCombinationsDto:
    json_encoder = object_to_json

    __shared_state = json_encoder(Turing.Api.Catalogs.Breakdowns.BreakdownsCombinations.BreakdownsCombinations())

    def __init__(self):
        self.__dict__ = self.__shared_state

    @classmethod
    def get(cls):
        return cls.__shared_state["combinations"]
