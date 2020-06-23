import sys
from io import StringIO

import pandas as pd
from googleads import adwords

from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Infrastructure.Domain.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from GoogleTuring.Infrastructure.Domain.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from GoogleTuring.Infrastructure.Mappings.AdWordsAPIInsightsMapper import AdWordsAPIInsightsMapper


class AdWordsAccountInsightsClient(AdWordsBaseClient):
    __ACCOUNT_FIELDS = [
        GoogleAttributeFieldsMetadata.account_descriptive_name,
        GoogleAttributeFieldsMetadata.external_customer_id,
        # direct manager
        # account type
        GoogleMetricFieldsMetadata.clicks,
        GoogleMetricFieldsMetadata.impressions,
        GoogleMetricFieldsMetadata.ctr,
        GoogleMetricFieldsMetadata.average_cpc,
        GoogleMetricFieldsMetadata.cost,
        GoogleMetricFieldsMetadata.conversions,
        GoogleMetricFieldsMetadata.conversion_rate,
        # account labels
        GoogleMetricFieldsMetadata.cost_per_conversion
    ]
    __REPORT = FiledGoogleInsightsTableEnum.ACCOUNT.value

    def get_account_insights(self, start_date, end_date):
        field_names = list(map(lambda x: x.field_name, self.__ACCOUNT_FIELDS))
        report_query = (adwords.ReportQueryBuilder()
                        .Select(*field_names)
                        .From(self.__REPORT)
                        .During(start_date=start_date, end_date=end_date)
                        .Build())

        report_data = StringIO()
        header = str(list(map(lambda x: x.name, self.__ACCOUNT_FIELDS)))
        header = header.replace(' ', '')
        header = header.replace('\'', '')
        header = header.replace('[', '')
        header = header.replace(']', '')
        report_data.write(header + '\n')

        stream_data = self.get_report_downloader().DownloadReportAsStreamWithAwql(
            report_query, 'CSV', skip_report_header=True, skip_column_header=True, skip_report_summary=True,
            include_zero_impressions=False)
        try:
            while True:
                chunk = stream_data.read(self._CHUNK_SIZE)
                if not chunk:
                    break
                report_data.write(
                    chunk.decode() if sys.version_info[0] == 3 and getattr(report_data, 'mode', 'w') == 'w' else chunk)
        finally:
            report_data.seek(0)
            df = pd.read_csv(report_data)
            df = AdWordsAPIInsightsMapper.map(fields=self.__ACCOUNT_FIELDS, df=df)

            report_data.close()
            stream_data.close()
            return df.to_dict('r')
