from enum import Enum


class Goals(Enum):
    CPC = 'CPC'
    CPM = 'CPM'
    CTR = 'CTR'
    Impressions = 'Impressions'
    Reach = 'Reach'
    Clicks = 'Clicks'
    CPP = 'CPP'
    # CPA = 'CPA'
    # ROAS = 'ROAS'

    # TODO: extend this if we need it later, else delete


goalDisplayNames = {
    "CPC": "Minimize Cost per Click",
    "CPM": "Minimize Cost per Mile",
    "CTR": "Maximize ClickTrough Rate",
    "CPA": "Minimize Cost per Action",
    "ROAS": "Maximize Return on Advertisment Spend"
}