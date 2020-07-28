from GoogleTuring.Api.Catalogs.ReportModels.Levels.Ad.AdReportEnum import AdReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.Levels.AdGroup.AdGroupReportEnum import AdGroupReportEnum
from GoogleTuring.Api.Catalogs.ReportModels.Levels.Campaign.CampaignReportEnum import CampaignReportEnum
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdDimensionColumnsMaster import AdDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdGroupDimensionColumnsMaster import \
    AdGroupDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdGroupMetricColumnsMaster import \
    AdGroupMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdGroupSegmentColumnsMaster import \
    AdGroupSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdMetricColumnsMaster import AdMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.AdSegmentColumnsMaster import AdSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.AdGroupAgeRangeDimensionColumnsMaster import \
    AdGroupAgeRangeDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.AdGroupAgeRangeMetricColumnsMaster import \
    AdGroupAgeRangeMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.AdGroupAgeRangeSegmentColumnsMaster import \
    AdGroupAgeRangeSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeDimensionColumnsMaster import \
    CampaignAgeRangeDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeMetricColumnsMaster import \
    CampaignAgeRangeMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeSegmentColumnsMaster import \
    CampaignAgeRangeSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.AdGroupGenderDimensionColumnsMaster import \
    AdGroupGenderDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.AdGroupGenderMetricColumnsMaster import \
    AdGroupGenderMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.AdGroupGenderSegmentColumnsMaster import \
    AdGroupGenderSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderDimensionColumnsMaster import \
    CampaignGenderDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderMetricColumnsMaster import \
    CampaignGenderMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderSegmentColumnsMaster import \
    CampaignGenderSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.AdGroupGeoDimensionColumnsMaster import \
    AdGroupGeoDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.AdGroupGeoMetricColumnsMaster import \
    AdGroupGeoMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.AdGroupGeoSegmentColumnsMaster import \
    AdGroupGeoSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.CampaignGeoDimensionColumnsMaster import \
    CampaignGeoDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.CampaignGeoMetricColumnsMaster import \
    CampaignGeoMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.CampaignGeoSegmentColumnsMaster import \
    CampaignGeoSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.AdGroupKeywordsDimensionColumnsMaster import \
    AdGroupKeywordsDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.AdGroupKeywordsMetricColumnsMaster import \
    AdGroupKeywordsMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.AdGroupKeywordsSegmentColumnsMaster import \
    AdGroupKeywordsSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.CampaignKeywordsDimensionColumnsMaster import \
    CampaignKeywordsDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.CampaignKeywordsMetricColumnsMaster import \
    CampaignKeywordsMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.CampaignKeywordsSegmentColumnsMaster import \
    CampaignKeywordsSegmentColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignDimensionColumnsMaster import \
    CampaignDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignMetricColumnsMaster import \
    CampaignMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignSegmentColumnsMaster import \
    CampaignSegmentColumnsMaster

REPORT_TO_DIMENSIONS = {
    CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT: CampaignDimensionColumnsMaster.DIMENSIONS,
    CampaignReportEnum.CAMPAIGN_GEO_PERFORMANCE_REPORT: CampaignGeoDimensionColumnsMaster.DIMENSIONS,
    CampaignReportEnum.CAMPAIGN_KEYWORDS_PERFORMANCE_REPORT: CampaignKeywordsDimensionColumnsMaster.DIMENSIONS,
    CampaignReportEnum.CAMPAIGN_GENDER_PERFORMANCE_REPORT: CampaignGenderDimensionColumnsMaster.DIMENSIONS,
    CampaignReportEnum.CAMPAIGN_AGE_RANGE_PERFORMANCE_REPORT: CampaignAgeRangeDimensionColumnsMaster.DIMENSIONS,
    AdGroupReportEnum.AD_GROUP_PERFORMANCE_REPORT: AdGroupDimensionColumnsMaster.DIMENSIONS,
    AdGroupReportEnum.AD_GROUP_GEO_PERFORMANCE_REPORT: AdGroupGeoDimensionColumnsMaster.DIMENSIONS,
    AdGroupReportEnum.AD_GROUP_KEYWORDS_PERFORMANCE_REPORT: AdGroupKeywordsDimensionColumnsMaster.DIMENSIONS,
    AdGroupReportEnum.AD_GROUP_GENDER_PERFORMANCE_REPORT: AdGroupGenderDimensionColumnsMaster.DIMENSIONS,
    AdGroupReportEnum.AD_GROUP_AGE_RANGE_PERFORMANCE_REPORT: AdGroupAgeRangeDimensionColumnsMaster.DIMENSIONS,
    AdReportEnum.AD_PERFORMANCE_REPORT: AdDimensionColumnsMaster.DIMENSIONS
}

REPORT_TO_METRICS = {
    CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT: CampaignMetricColumnsMaster().DIMENSION_TO_METRICS,
    CampaignReportEnum.CAMPAIGN_GEO_PERFORMANCE_REPORT: CampaignGeoMetricColumnsMaster().DIMENSION_TO_METRICS,
    CampaignReportEnum.CAMPAIGN_KEYWORDS_PERFORMANCE_REPORT: CampaignKeywordsMetricColumnsMaster().DIMENSION_TO_METRICS,
    CampaignReportEnum.CAMPAIGN_GENDER_PERFORMANCE_REPORT: CampaignGenderMetricColumnsMaster().DIMENSION_TO_METRICS,
    CampaignReportEnum.CAMPAIGN_AGE_RANGE_PERFORMANCE_REPORT: CampaignAgeRangeMetricColumnsMaster().DIMENSION_TO_METRICS,
    AdGroupReportEnum.AD_GROUP_PERFORMANCE_REPORT: AdGroupMetricColumnsMaster().DIMENSION_TO_METRICS,
    AdGroupReportEnum.AD_GROUP_GEO_PERFORMANCE_REPORT: AdGroupGeoMetricColumnsMaster().DIMENSION_TO_METRICS,
    AdGroupReportEnum.AD_GROUP_KEYWORDS_PERFORMANCE_REPORT: AdGroupKeywordsMetricColumnsMaster().DIMENSION_TO_METRICS,
    AdGroupReportEnum.AD_GROUP_GENDER_PERFORMANCE_REPORT: AdGroupGenderMetricColumnsMaster().DIMENSION_TO_METRICS,
    AdGroupReportEnum.AD_GROUP_AGE_RANGE_PERFORMANCE_REPORT: AdGroupAgeRangeMetricColumnsMaster().DIMENSION_TO_METRICS,
    AdReportEnum.AD_PERFORMANCE_REPORT: AdMetricColumnsMaster().DIMENSION_TO_METRICS
}

REPORT_TO_BREAKDOWNS = {
    CampaignReportEnum.CAMPAIGN_PERFORMANCE_REPORT: CampaignSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    CampaignReportEnum.CAMPAIGN_GEO_PERFORMANCE_REPORT: CampaignGeoSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    CampaignReportEnum.CAMPAIGN_KEYWORDS_PERFORMANCE_REPORT: CampaignKeywordsSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    CampaignReportEnum.CAMPAIGN_GENDER_PERFORMANCE_REPORT: CampaignGenderSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    CampaignReportEnum.CAMPAIGN_AGE_RANGE_PERFORMANCE_REPORT: CampaignAgeRangeSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    AdGroupReportEnum.AD_GROUP_PERFORMANCE_REPORT: AdGroupSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    AdGroupReportEnum.AD_GROUP_GEO_PERFORMANCE_REPORT: AdGroupGeoSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    AdGroupReportEnum.AD_GROUP_KEYWORDS_PERFORMANCE_REPORT: AdGroupKeywordsSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    AdGroupReportEnum.AD_GROUP_GENDER_PERFORMANCE_REPORT: AdGroupGenderSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    AdGroupReportEnum.AD_GROUP_AGE_RANGE_PERFORMANCE_REPORT: AdGroupAgeRangeSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS,
    AdReportEnum.AD_PERFORMANCE_REPORT: AdSegmentColumnsMaster().DIMENSION_TO_METRIC_TO_SEGMENTS
}
