from Algorithms.Models.Types import TypesWrapper as Tw
from Algorithms.Tools import ColumnsEnum, Columns
from Algorithms.Tools.TimeInterval import TimeInterval
from Config.DbData import ExternalTables, DetailsTables
from Infrastructure.QueryBuilder import QueryBuilder as Qb, Authorization


# TODO: Like Mongo, make this static to ensure there is only one connection
class QueryBuilderMediator(object):
    """Used to create queries from optimization types"""

    def __init__(self, token):
        self.__end_point = ExternalTables.ENDPOINT.value
        if token is None:
            self.__authorization_token = Authorization.get_authorization_token()
        else:
            self.__authorization_token = token

    def get_goals(self):
        # TODO : remove Magic Strings
        helper = Qb.QueryBuilderHelper(self.__end_point, "Campaigns", self.__authorization_token)
        dimensions = [{"GroupColumnName": "id"}, {"GroupColumnName": "Goal"}]
        response = helper.send_query(None, dimensions, None)
        return response.json()

    def get_details(self, ad_account_id, level):
        # TODO : remove Magic Strings
        table_name = DetailsTables[level].value
        helper = Qb.QueryBuilderHelper(self.__end_point, table_name, self.__authorization_token)
        dimensions = [{"GroupColumnName": "id"}, {"GroupColumnName": "FacebookDetails"}, {"GroupColumnName": "AdAccountId"}]
        ad_account_filter = helper.get_filter_block(["act_" + str(ad_account_id)], "AdAccountId")
        if level == Tw.LevelNames.AdSet.value:
            dimensions.append({"GroupColumnName": "CampaignId"})
        if level == Tw.LevelNames.Ad.value:
            dimensions.append({"GroupColumnName": "CampaignId"})
            dimensions.append({"GroupColumnName": "AdSetId"})

        # TODO: Query the facebook instead of SQL server
        response = helper.send_query(None, dimensions, ad_account_filter)
        details_json = response.json()

        return details_json

    def get_actor_states(self, ad_account_id):
        # TODO : remove Magic Strings        
        helper = Qb.QueryBuilderHelper(self.__end_point, ExternalTables.ACTOR_STATES.value, self.__authorization_token)
        dimensions = [{"GroupColumnName": "id"}, {"GroupColumnName": "StateId"}, {"GroupColumnName": "Level"}]
        ad_account_filter = helper.get_filter_block(["act_" + str(ad_account_id)], "AdAccountId")
        response = helper.send_query(None, dimensions, ad_account_filter)
        states_json = response.json()
        return states_json

    def get_data_for_optimization_tuple(self, optimization: Tw.OptimizationTuple, time_interval: TimeInterval, ad_account_id):
        if optimization.breakdown in [Tw.LevelNames.Breakdown.value]:
            table_name = ExternalTables['AdSet'].value
        else:
            table_name = ExternalTables[optimization.breakdown].value

        helper = Qb.QueryBuilderHelper(self.__end_point, table_name, self.__authorization_token)

        where_clause = self.__get_where_clause(optimization, helper, time_interval, ad_account_id)
        dimensions = self.__get_group_by(optimization)
        columns = self.__get_columns(optimization)

        response = helper.send_query(columns, dimensions, where_clause)
        if response.status_code >= 400:
            raise ValueError(response.text)
        insights_json = response.json()
        insights_json = self.__get_insights_json_with_iso_date(insights_json)
        return insights_json

    def __get_where_clause(self, optimization: Tw.OptimizationTuple, helper: Qb.QueryBuilderHelper, time_interval: TimeInterval, ad_account_id):
        start_date = time_interval.get_start_date_string()
        end_date = time_interval.get_end_date_string()
        time_filter_b_lock = helper.get_time_block(start_date, end_date, ColumnsEnum.Where.DATE.value)
        sql_ad_account_id = "act_" + ad_account_id
        ad_account_block = helper.get_filter_block([sql_ad_account_id], ColumnsEnum.Where.AD_ACCOUNT_ID.value)
        ad_account_and_time_block = helper.link_filter_blocks(time_filter_b_lock, ad_account_block)

        if optimization.breakdown == Tw.Levels.Interest.name:
            return ad_account_and_time_block

        breakdown_filter_block = helper.get_filter_block([Columns.breakdown_name_to_id_mapping[optimization.action_breakdown]], ColumnsEnum.Where.BREAKDOWN_ID.value)
        action_break_down_block = helper.get_filter_block([0], ColumnsEnum.Where.ACTION_BREAKDOWN_ID.value)
        linked_block = Qb.QueryBuilderHelper.link_filter_blocks(ad_account_and_time_block, breakdown_filter_block)
        linked_block = Qb.QueryBuilderHelper.link_filter_blocks(linked_block, action_break_down_block)
        return linked_block

    def __get_columns(self, optimization: Tw.OptimizationTuple):
        columns = Columns.get_columns(optimization)["Columns"]
        return columns

    def __get_group_by(self, optimization: Tw.OptimizationTuple):
        group_bys = Columns.get_columns(optimization)["Dimensions"]
        dimensions = []
        for dimension in group_bys:
            dimensions.append({"GroupColumnName": dimension})
        return dimensions

    def __get_insights_json_with_iso_date(self, response_insights):
        for insight in response_insights:
            insight_time = insight[ColumnsEnum.Where.DATE.value]
            insight[ColumnsEnum.Where.DATE.value] = TimeInterval.get_date_time_object(insight_time)
        return response_insights
