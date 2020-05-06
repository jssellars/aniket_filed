from Core.Metadata.Views.ViewBase import View


class GoogleView(View):
    data_source_name = None
    breakdowns = {
        "segments": []
    }
