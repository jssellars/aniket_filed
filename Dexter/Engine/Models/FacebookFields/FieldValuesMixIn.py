from Packages.Tools.ObjectManipulators import extract_class_attributes_values


class Level:
    campaign = "campaign"
    adset = "adset"
    ad = "ad"

    @classmethod
    def get_levels(cls):
        return extract_class_attributes_values(cls)


class LevelStructuresEnum:
    campaign = "campaigns"
    adset = "adsets"
    ad = "ads"


class TimeRange:
    since = "since"
    until = "until"


class TimeInterval:
    dateStart = "date_start"
    dateStop = "date_stop"
    increment = "time_increment"
