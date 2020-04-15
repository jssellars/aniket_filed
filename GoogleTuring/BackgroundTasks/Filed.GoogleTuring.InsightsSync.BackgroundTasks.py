import sys
from datetime import datetime
from io import StringIO

import pandas as pd
from dateutil.relativedelta import relativedelta
from googleads import adwords

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Web.GoogleAdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.Infrastructure.Domain.Enums.ActionBreakdown import ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Breakdown import BreakdownType, BREAKDOWN_TO_FIELD, DEFAULT_TIME_BREAKDOWN_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Level import LEVEL_TO_IDENTIFIER
from GoogleTuring.Infrastructure.Domain.Insights.Breakdowns.GoogleAgeRangeInsightsDefinition import GoogleAgeInsightsDefinition
from GoogleTuring.Infrastructure.Domain.Insights.Breakdowns.GoogleGenderInsightsDefinition import GoogleGenderInsightsDefinition
from GoogleTuring.Infrastructure.Domain.Insights.Breakdowns.GoogleKeywordsInsightsDefinition import GoogleKeywordsInsightsDefinition
from GoogleTuring.Infrastructure.Domain.Insights.Levels.GoogleAdGroupInsightsDefinition import GoogleAdGroupInsightsDefinition
from GoogleTuring.Infrastructure.Domain.Insights.Levels.GoogleAdInsighstDefinition import GoogleAdInsightsDefinition
from GoogleTuring.Infrastructure.Domain.Insights.Levels.GoogleCampaignInsightsDefinition import GoogleCampaignInsightsDefinition
from GoogleTuring.Infrastructure.PersistanceLayer.GoogleTuringInsightsMongoRepository import GoogleTuringInsightsMongoRepository

CHUNK_SIZE = 16 * 1024


def main():
    client = AdWordsBaseClient(config=startup.google_config)
    report_downloader = client.get_report_downloader()

    mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
    mongo_repository = GoogleTuringInsightsMongoRepository(client=mongo_conn_handler.client, database_name=startup.mongo_config['googleInsightsDatabaseName'],
                                                           location_collection_name=startup.mongo_config['locationDataCollectionName'])

    end_date = datetime.now()
    start_date = end_date - relativedelta(months=6)

    insights_definitions = [
        GoogleKeywordsInsightsDefinition(),
        GoogleGenderInsightsDefinition(),
        GoogleAgeInsightsDefinition(),

        GoogleAdInsightsDefinition(),
        GoogleAdGroupInsightsDefinition(),
        GoogleCampaignInsightsDefinition()
    ]

    insights_data_list = []
    insights_breakdown_type = []

    for insights_definition in insights_definitions:
        report_name = insights_definition.table_name

        if insights_definition.breakdowns is None:
            for action_breakdown in insights_definition.action_breakdowns:
                fields = insights_definition.fields[action_breakdown]
                print('Starting on {}-{}-{}'.format(insights_definition.level.value, 'none', action_breakdown.value))

                compound_fields, required_fields = extract_compound_and_required_fields(fields)
                join_fields = list(filter(lambda x: x is not None and x.join_condition is not None, fields))
                filtered_fields = list(filter(lambda x: x is not None and x.field_name is not None, fields))

                filtered_fields.extend(required_fields)
                df = create_dataframe(filtered_fields, report_downloader, report_name, start_date, end_date)
                if join_fields:
                    df = create_join_dataframe(df_to_join=df, join_fields=join_fields, breakdown=None, action_breakdown=action_breakdown, level=insights_definition.level,
                                               report_downloader=report_downloader, report_name=report_name,
                                               start_date=start_date, end_date=end_date)

                collection_name = insights_definition.level.value + '-none-' + action_breakdown.value
                insights_data_list.append((collection_name, df, filtered_fields, compound_fields))
                insights_breakdown_type.append((insights_definition.breakdowns, insights_definition.breakdown_type))

        else:
            for level in insights_definition.levels:
                for breakdown in insights_definition.breakdowns:
                    for action_breakdown in insights_definition.action_breakdowns:
                        print('Starting on {}-{}-{}'.format(level.value, breakdown.value, action_breakdown.value))
                        fields = insights_definition.fields[level][breakdown][action_breakdown]

                        compound_fields, required_fields = extract_compound_and_required_fields(fields)
                        join_fields = list(filter(lambda x: x is not None and x.join_condition is not None, fields))
                        filtered_fields = list(filter(lambda x: x is not None and x.field_name is not None, fields))
                        filtered_fields.extend(required_fields)

                        df = create_dataframe(filtered_fields, report_downloader, report_name, start_date, end_date)
                        if join_fields:
                            df = create_join_dataframe(df_to_join=df, join_fields=join_fields, breakdown=breakdown, action_breakdown=action_breakdown, level=level,
                                                       report_downloader=report_downloader, report_name=report_name,
                                                       start_date=start_date, end_date=end_date)
                        collection_name = level.value + '-' + breakdown.value + '-' + action_breakdown.value
                        insights_data_list.append((collection_name, df, filtered_fields, compound_fields))
                        insights_breakdown_type.append((breakdown, insights_definition.breakdown_type))

    for insights_data, breakdown_data in zip(insights_data_list, insights_breakdown_type):
        collection_name, df, filtered_fields, compound_fields = insights_data
        breakdown, breakdown_type = breakdown_data
        if breakdown_type == BreakdownType.GEO_BREAKDOWN:
            mongo_repository.update_locations_if_needed(df, breakdown, client)

        mongo_repository.insert_insights_into_db(collection_name, df, filtered_fields, compound_fields)

    print('BT DONE!')


def create_dataframe(fields, report_downloader, report_name, start_date, end_date):
    report_query = (adwords.ReportQueryBuilder()
                    .Select(*map(lambda x: x.field_name, fields))
                    .From(report_name)
                    .Where('CampaignStatus').In('ENABLED', 'PAUSED')
                    .During(start_date=start_date, end_date=end_date)
                    .Build())

    report_data = StringIO()

    header = list(map(lambda x: x.name, fields))
    header = str(header).replace(' ', '')
    header = str(header).replace('\'', '')
    header = str(header).replace('[', '')
    header = str(header).replace(']', '')
    report_data.write(header + '\n')
    stream_data = report_downloader.DownloadReportAsStreamWithAwql(
        report_query, 'CSV', skip_report_header=True,
        skip_column_header=True, skip_report_summary=True, include_zero_impressions=False)
    try:
        while True:
            chunk = stream_data.read(CHUNK_SIZE)
            if not chunk:
                break
            report_data.write(chunk.decode() if sys.version_info[0] == 3 and getattr(report_data, 'mode', 'w') == 'w' else chunk)
    finally:
        report_data.seek(0)
        df = pd.read_csv(report_data)
        report_data.close()
        stream_data.close()
    return df


def create_join_dataframe(df_to_join, join_fields, breakdown, action_breakdown, level, report_downloader, report_name, start_date, end_date):
    for join_field in join_fields:
        field_name = join_field.name
        join_condition = join_field.join_condition

        equal_to = join_condition.equal_to
        target_field = join_condition.target_field
        compare_field = join_condition.compare_field
        identifier = LEVEL_TO_IDENTIFIER[level]

        select_list = [identifier.field_name, target_field.field_name, compare_field.field_name, DEFAULT_TIME_BREAKDOWN_FIELD.field_name]
        action_breakdown_field = ACTION_BREAKDOWN_TO_FIELD[action_breakdown]
        if breakdown:
            breakdown_field = BREAKDOWN_TO_FIELD[breakdown]
            select_list.append(breakdown_field.field_name)

        if action_breakdown_field:
            select_list.append(action_breakdown_field.field_name)

        report_query = (adwords.ReportQueryBuilder()
                        .Select(*select_list)
                        .From(report_name)
                        .Where('CampaignStatus').In('ENABLED', 'PAUSED')
                        .Where(compare_field.field_name).EqualTo(equal_to)
                        .During(start_date=start_date, end_date=end_date)
                        .Build())

        report_data = StringIO()
        header = [identifier.name, field_name, compare_field.name, DEFAULT_TIME_BREAKDOWN_FIELD.name]

        if breakdown:
            breakdown_field = BREAKDOWN_TO_FIELD[breakdown]
            header.append(breakdown_field.name)

        if action_breakdown_field:
            header.append(action_breakdown_field.name)

        header = str(header).replace(' ', '')
        header = str(header).replace('\'', '')
        header = str(header).replace('[', '')
        header = str(header).replace(']', '')
        report_data.write(header + '\n')
        stream_data = report_downloader.DownloadReportAsStreamWithAwql(
            report_query, 'CSV', skip_report_header=True,
            skip_column_header=True, skip_report_summary=True, include_zero_impressions=False)
        try:
            while True:
                chunk = stream_data.read(CHUNK_SIZE)
                if not chunk:
                    break
                report_data.write(chunk.decode() if sys.version_info[0] == 3 and getattr(report_data, 'mode', 'w') == 'w' else chunk)
        finally:
            report_data.seek(0)
            df = pd.read_csv(report_data)
            df = df.drop(columns=compare_field.field_name)
            report_data.close()
            stream_data.close()

            on_keys = [identifier.name, DEFAULT_TIME_BREAKDOWN_FIELD.name]
            if action_breakdown_field:
                on_keys.append(action_breakdown_field.name)

            if breakdown:
                breakdown_field = BREAKDOWN_TO_FIELD[breakdown]
                on_keys.append(breakdown_field.name)

            df_to_join = pd.merge(df_to_join, df, how='left', on=on_keys)

    return df_to_join


def extract_compound_and_required_fields(fields):
    compound_fields = []
    required_fields = []

    for field in fields:
        if field is not None and field.required_fields is not None:
            compound_fields.append(field)
            required_fields.extend(field.required_fields)

    return compound_fields, required_fields


if __name__ == '__main__':
    main()
