from Algorithms.Tools.BreakdownsGetter import create_all_level_breakdown_combinations
from Algorithms.Tools.TimeInterval import TimeInterval
from Obsolete.CampaignGoals.Seeding import DefinitionsSeeder
from Algorithms.Tools.InsightsSyncing.Synchronizer import Synchronizer

# TODO: Deprecated, should remove in the future.
def sync_prophet_data(budgetTypes_, date_range):
    for interType in budgetTypes_:
        data = mongoMediator.get_data_for_prophet(interType, date_range)
        data_for_opt_df = pd.DataFrame(data)
        end_date = date_range.get_end_date_string("%x").replace('/', '_')
        data_for_opt_df.to_csv(f'D:/CSVProphetData/{interType.Level}.csv')

# TODO: Deprecated, should remove in the future.
def synchronize(date_range: TimeInterval, ad_account_id, token):
    # get data from sql into mongo
    syncrhonizer = Synchronizer(token, mongo_mediator=mongoMediator)

    all_data_types = create_all_level_breakdown_combinations()

    for inter_type in all_data_types:
        syncrhonizer.sync_data_for_type(inter_type, date_range, ad_account_id)

    syncrhonizer.update_actor_states(ad_account_id)

# TODO: Deprecated, should remove in the future.
def seed_goals():
    DefinitionsSeeder.SeedGoals()