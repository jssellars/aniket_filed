from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewMaster(View):
    name = "Master"
    table_name = "vCampaignInsights"
    type = "Master"
    columns = extract_class_attributes_values(ViewColumnsMaster)
