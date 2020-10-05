from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from FacebookTuring.Api.Catalogs.Breakdowns.ActionBreakdowns import ActionBreakdowns
from FacebookTuring.Api.Catalogs.Breakdowns.DeliveryBreakdowns import DeliveryBreakdowns
from FacebookTuring.Api.Catalogs.Breakdowns.TimeBreakdowns import TimeBreakdowns

REPORTS_BREAKDOWNS = {
    "action": extract_class_attributes_values(ActionBreakdowns),
    "delivery": extract_class_attributes_values(DeliveryBreakdowns),
    "time": extract_class_attributes_values(TimeBreakdowns)
}
