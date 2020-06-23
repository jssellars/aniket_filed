import sys
from io import StringIO

import pandas as pd
from googleads import adwords

from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.Infrastructure.Mappings.AdWordsAPIInsightsMapper import AdWordsAPIInsightsMapper


class AdWordsInsightsClient(AdWordsBaseClient):
    def get_insights(self, report_name, status_field, fields, start_date, end_date, skip_summary=True):
        status_field_name = status_field.field_name
        field_names = list(map(lambda x: x.field_name, fields))
        report_query = (adwords.ReportQueryBuilder()
                        .Select(*field_names)
                        .From(report_name)
                        .Where(status_field_name).In('ENABLED', 'PAUSED')
                        .During(start_date=start_date, end_date=end_date)
                        .Build())

        report_data = StringIO()

        header = field_names
        header = str(header).replace(' ', '')
        header = header.replace('\'', '')
        header = header.replace('[', '')
        header = header.replace(']', '')
        report_data.write(header + '\n')

        stream_data = self.get_report_downloader().DownloadReportAsStreamWithAwql(
            report_query, 'CSV', skip_report_header=True, skip_column_header=True, skip_report_summary=skip_summary,
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
            df = AdWordsAPIInsightsMapper.map(fields=fields, df=df)

            report_data.close()
            stream_data.close()
        if skip_summary:
            return df.to_dict('r')
        else:
            report = df.to_dict('r')
            data = report[:-1]

            summary = report[-1]
            # remove 'Total' value from summary
            summary[fields[0].field_name] = None
            return {'data': data, 'summary': summary}

    def get_insights_with_totals(self, report_name, status_field, fields, start_date, end_date):
        return self.get_insights(report_name, status_field, fields, start_date, end_date, skip_summary=False)
