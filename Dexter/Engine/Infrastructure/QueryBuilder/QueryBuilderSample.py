import json

from Config import DbData
from Infrastructure.QueryBuilder import Authorization as Auth
from Infrastructure.QueryBuilder import QueryBuilder

authorization_token = Auth.get_authorization_token()

# Provide dummy object to build columns
x = {
    'Impressions': 200
}
columns = QueryBuilder.QueryBuilderHelper.get_columns(x, QueryBuilder.ColumnAggregator.sum)

# Provide necessary QueryBuilder data.
# TODO: de-reference DbData, making the sample ( and the package as a whole ) project agnostic
campaign_url = DbData.ExternalTables.ENDPOINT
table_name = DbData.ExternalTables.CAMPAIGN.value
helper = QueryBuilder.QueryBuilderHelper(campaign_url, table_name, authorization_token)

# Create nested Filter block (where clause)
column_name = 'FacebookId'
child_block = helper.get_filter_block(['23843237677730464', '23843237733230464'], column_name)
time_block = helper.get_time_block("2019-07-01", "2019-07-15", "Parameters_Until")
new_block = QueryBuilder.QueryBuilderHelper.link_filter_blocks(time_block, child_block)

# Specify Group By clause
dimensions = ['name']

# Look at the query being built
query = helper._build_query(columns, dimensions, new_block)
json.dumps(query)

# Build and send query
response = helper.send_query(columns, dimensions, new_block)

print(response.text)
