import Turing.Api.Catalogs.Breakdowns.ActionBreakdowns
import Turing.Api.Catalogs.Breakdowns.DeliveryBreakdowns
import Turing.Api.Catalogs.Breakdowns.TimeBreakdowns
from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from FacebookTuring.Api.Catalogs.Breakdowns.BreakdownsCombinations import BreakdownsCombinations
from FacebookTuring.Api.Catalogs.Views.ViewMaster import ViewMaster


class AdsManagerCatalogsMetacolumnsDto:

    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    __shared_state = {
        "masterView": json_encoder(ViewMaster()),
        "breakdowns": {
            "action": json_list_encoder(Turing.Api.Catalogs.Breakdowns.ActionBreakdowns.ActionBreakdowns()),
            "delivery": json_list_encoder(Turing.Api.Catalogs.Breakdowns.DeliveryBreakdowns.DeliveryBreakdowns()),
            "time": json_list_encoder(Turing.Api.Catalogs.Breakdowns.TimeBreakdowns.TimeBreakdowns())
        },
        "breakdownCombinations": json_list_encoder(BreakdownsCombinations())
    }

    def __init__(self):
        self.__dict__ = self.__shared_state


    @classmethod
    def get(cls):
        return cls.__shared_state
