from Core.Metadata.Views.ViewBase import BaseView


class GoogleView(BaseView):
    data_source_name = None
    breakdowns = {
        "segments": []
    }
