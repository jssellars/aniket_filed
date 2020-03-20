from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewMaster(View):
    name = "Master"
    table_name = "vCampaignInsights"
    type = "Master"
    columns = extract_class_attributes_values(ViewColumnsMaster)