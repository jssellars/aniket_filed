import sys
from io import StringIO

import pandas as pd
from googleads import adwords

from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import QueryBuilderLogicalOperator
from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.Infrastructure.Domain.Enums.Level import LEVEL_TO_IDENTIFIER
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Infrastructure.Mappings.AdWordsAPIAccountInsightsMapper import AdWordsAPIInsightsMapper


class AdWordsInsightsClient(AdWordsBaseClient):
    __TIME_INCREMENT_TO_FIELD = {
        # default -> all days
        1: GoogleFieldsMetadata.date,
        7: GoogleFieldsMetadata.week,
        30: GoogleFieldsMetadata.month
    }

    __CONDITION_MAPPING = {
        QueryBuilderLogicalOperator.EQUAL:
            lambda report_query, field, value: report_query.Where(field).EqualTo(value),
        QueryBuilderLogicalOperator.GREATER_THAN:
            lambda report_query, field, value: report_query.Where(field).GreaterThan(value),
        QueryBuilderLogicalOperator.GREATER_THAN_OR_EQUAL:
            lambda report_query, field, value: report_query.Where(field).GreaterThanOrEqualTo(value),
        QueryBuilderLogicalOperator.LESS_THAN:
            lambda report_query, field, value: report_query.Where(field).LessThan(value),
        QueryBuilderLogicalOperator.LESS_THAN_OR_EQUAL:
            lambda report_query, field, value: report_query.Where(field).LessThanOrEqualTo(value),
        QueryBuilderLogicalOperator.NOT_EQUAL:
            lambda report_query, field, value: report_query.Where(field).NotIn(*value),
        QueryBuilderLogicalOperator.IN:
            lambda report_query, field, value: report_query.Where(field).In(*value),

    }

    def get_insights(self, report_name, status_field, fields, start_date, end_date, time_increment, filtering, level,
                     skip_summary=True):
        remove_identifier = False
        status_field_name = status_field.field_name
        time_increment_field = self.__TIME_INCREMENT_TO_FIELD.get(time_increment)
        identifier = LEVEL_TO_IDENTIFIER[level]

        join_fields = list(filter(lambda x: x is not None and x.join_condition is not None, fields))
        filtered_fields = list(filter(lambda x: x is not None and x.field_name is not None, fields))
        report_downloader = self.get_report_downloader()

        if identifier not in fields and join_fields:
            filtered_fields.append(identifier)
            remove_identifier = True

        df = self.__create_base_dataframe(fields=filtered_fields, report_downloader=report_downloader,
                                          report_name=report_name, start_date=start_date, end_date=end_date,
                                          time_increment_field=time_increment_field,
                                          status_field_name=status_field_name, filtering=filtering,
                                          skip_summary=skip_summary)
        if join_fields:
            df = self.__join_dataframes(df_to_join=df, join_fields=join_fields,
                                        identifier=identifier,
                                        report_downloader=report_downloader, report_name=report_name,
                                        start_date=start_date, end_date=end_date,
                                        time_increment_field=time_increment_field,
                                        status_field_name=status_field_name,
                                        filtering=filtering,
                                        skip_summary=skip_summary)

        if remove_identifier:
            df = df.drop(identifier.name, axis=1)

        df = AdWordsAPIInsightsMapper.map(fields=fields, df=df)
        if skip_summary:
            return df.to_dict('r')
        else:
            report = df.to_dict('r')
            data = report[:-1]

            summary = report[-1]
            # remove 'Total' value from summary
            summary[fields[0].name] = None
            return {'data': data, 'summary': summary}

    def get_insights_with_totals(self, report_name, status_field, fields, start_date, end_date, time_increment,
                                 filtering, level):
        return self.get_insights(report_name, status_field, fields, start_date, end_date, time_increment, filtering,
                                 level, skip_summary=False)

    def __create_base_dataframe(self, fields, report_downloader, report_name, start_date, end_date,
                                time_increment_field, status_field_name, filtering, skip_summary):
        if time_increment_field:
            select_fields = fields + [time_increment_field]
        else:
            select_fields = fields

        report_query = (adwords.ReportQueryBuilder()
                        .Select(*map(lambda x: x.field_name, select_fields))
                        .From(report_name)
                        .Where(status_field_name).In('ENABLED', 'PAUSED')
                        .During(start_date=start_date, end_date=end_date))

        report_query = self.__build_query_conditions(report_query, filtering)

        report_data = StringIO()
        header = list(map(lambda x: x.name, select_fields))
        header = str(header).replace(' ', '')
        header = str(header).replace('\'', '')
        header = str(header).replace('[', '')
        header = str(header).replace(']', '')
        report_data.write(header + '\n')

        stream_data = report_downloader.DownloadReportAsStreamWithAwql(
            report_query, 'CSV', skip_report_header=True,
            skip_column_header=True, skip_report_summary=skip_summary, include_zero_impressions=False)
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
            report_data.close()
            stream_data.close()
        return df

    def __join_dataframes(self, df_to_join, join_fields, identifier, report_downloader,
                          report_name, start_date, end_date, time_increment_field, status_field_name, filtering,
                          skip_summary):
        for join_field in join_fields:
            field_name = join_field.name
            join_condition = join_field.join_condition

            equal_to = join_condition.equal_to
            target_field = join_condition.target_field
            compare_field = join_condition.compare_field

            select_list = [identifier.field_name, target_field.field_name]
            header = [identifier.name, field_name]
            on_keys = [identifier.name]
            if time_increment_field:
                select_list.append(time_increment_field.field_name)
                header.append(time_increment_field.name)
                on_keys.append(time_increment_field.name)

            report_query = (adwords.ReportQueryBuilder()
                            .Select(*select_list)
                            .From(report_name)
                            .Where(status_field_name).In('ENABLED', 'PAUSED')
                            .Where(compare_field.field_name).EqualTo(equal_to)
                            .During(start_date=start_date, end_date=end_date))
            report_query = self.__build_query_conditions(report_query, filtering)

            report_data = StringIO()
            header = str(header).replace(' ', '')
            header = str(header).replace('\'', '')
            header = str(header).replace('[', '')
            header = str(header).replace(']', '')
            report_data.write(header + '\n')
            stream_data = report_downloader.DownloadReportAsStreamWithAwql(
                report_query, 'CSV', skip_report_header=True,
                skip_column_header=True, skip_report_summary=skip_summary, include_zero_impressions=False)
            try:
                while True:
                    chunk = stream_data.read(self._CHUNK_SIZE)
                    if not chunk:
                        break
                    report_data.write(
                        chunk.decode() if sys.version_info[0] == 3 and getattr(report_data, 'mode',
                                                                               'w') == 'w' else chunk)
            finally:
                report_data.seek(0)
                df = pd.read_csv(report_data)
                report_data.close()
                stream_data.close()
                df_to_join = pd.merge(df_to_join, df, how='left', on=on_keys)

        return df_to_join

    def __build_query_conditions(self, report_query, filtering):
        for google_filter in filtering:
            report_query = self.__CONDITION_MAPPING[google_filter.operator](report_query, google_filter.field,
                                                                            google_filter.value)
        return report_query.Build()
