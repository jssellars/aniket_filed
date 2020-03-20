import Turing.Api.Catalogs.Breakdowns.ActionBreakdowns
import Turing.Api.Catalogs.Breakdowns.DeliveryBreakdowns
import Turing.Api.Catalogs.Breakdowns.TimeBreakdowns
from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list


class AdsManagerCatalogsBreakdownsDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    __shared_state = {
        "action": json_list_encoder(Turing.Api.Catalogs.Breakdowns.ActionBreakdowns.ActionBreakdowns()),
        "delivery": json_list_encoder(Turing.Api.Catalogs.Breakdowns.DeliveryBreakdowns.DeliveryBreakdowns()),
        "time": json_list_encoder(Turing.Api.Catalogs.Breakdowns.TimeBreakdowns.TimeBreakdowns())
    }

    def __init__(self):
        super().__init__()
        self.__dict__ = self.__shared_state

    @classmethod
    def get(cls):
        return cls.__shared_state
