from Core.Metadata.Views.ViewBase import View
from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewMaster(View):
    view_name = "Master"
    table_name = "vCampaignInsights"
    type = "Master"
    columns = extract_class_attributes_values(ViewColumnsMaster)
