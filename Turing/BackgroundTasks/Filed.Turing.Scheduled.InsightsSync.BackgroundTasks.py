import json
from datetime import datetime, timedelta

from Orchestrators import Orchestrator, OrchestratorRunConfig
from Orchestrators import AdInsightsSyncJobDefinition
from Orchestrators import AdSetInsightsSyncJobDefinition
from Orchestrators import CampaignInsightsSyncJobDefinition
from Turing.Infrastructure import TuringMongoRepository
from Mappers.AdSetStructureMapper import AdSetStructureMapper
from Mappers.AdStructureMapper import AdStructureMapper
from Mappers.CampaignStructureMapper import CampaignStructureMapper
from Turing.Infrastructure.Models.FacebookFieldValuesMixIn import Level
from Packages import BaseFacebookAdsApi
from Packages import MongoConnectionHandler
from Packages import BusinessOwnerTokenHelper
from Turing.BackgroundTasks.Startup import Startup

# TODO: get list of Business Owners Fields Ids + corresponding ad account Fields Ids from database
accountsLatestState = [
    {
        "business_owner_facebook_id": "1623950661230875",
        "ad_account_ids": ["act_2066904460189854",
                           "act_273538789947186",
                           "act_756882231399117",
                           "act_1726846407528996",
                           "act_1522264168066192",
                           "act_62854450",
                           "act_514788759380733",
                           "act_453013902026514",
                           "act_523866785010583",
                           "act_1348456131991886",
                           "act_1136117409921306",
                           "act_356835871471391",
                           "act_389109158588065",
                           "act_1795121250535778",
                           "act_115668799301458",
                           "act_1982676575279310",
                           "act_1966256986921269",
                           "act_1921637134716588",
                           "act_1898397830373852",
                           "act_1810325822514387",
                           "act_714733279004034",
                           "act_1041694276163579",
                           "act_403857376982920",
                           "act_29574895",
                           "act_14448834",
                           "act_420746395484759",
                           "act_124678721325114",
                           "act_984943871564834",
                           "act_489047665079827",
                           "act_579156189515811",
                           "act_665397517306957",
                           "act_52127988",
                           "act_2531947207050270",
                           "act_546802906163749",
                           "act_637388243672313",
                           "act_1203618286381384",
                           "act_3074226902607410",
                           "act_538942033602727",
                           "act_2505368132876242",
                           "act_283933757",
                           "act_2217439038501148",
                           "act_2345831895666522",
                           "act_609017073195410",
                           "act_525710184566414",
                           "act_559311931217427",
                           "act_1387250608265689",
                           "act_10152082108717909",
                           "act_37797914",
                           "act_481818525716780",
                           "act_261875116",
                           "act_792365617496376",
                           "act_1303535869712679",
                           "act_1248068512052076",
                           "act_2242745292656390",
                           "act_106506703305621",
                           "act_105040943196986",
                           "act_402941286797810",
                           "act_2451045728542434",
                           ]
    }
]


with open('Config/Settings/app.settings.dev.json', 'r') as appSettingsJsonFile:
    appConfig = json.load(appSettingsJsonFile)
startup = Startup(appConfig)

syncInsightsJobsDefinitionsFactory = {
    Level.campaign: CampaignInsightsSyncJobDefinition,
    Level.adset: AdSetInsightsSyncJobDefinition,
    Level.ad: AdInsightsSyncJobDefinition
}

mapperFactory = {
    Level.campaign: CampaignStructureMapper(),
    Level.adset: AdSetStructureMapper(),
    Level.ad: AdStructureMapper()
}

# Create Mongo repository
client = MongoConnectionHandler(startup.mongoConfig)
mongoRepository = TuringMongoRepository(client=client.client,
                                        databaseName=startup.mongoConfig['insightsDatabaseName'])

levels = Level.get_levels()
levels.reverse()

absolute_date_start = datetime(2019, 9, 1)
absolute_date_stop = datetime.now()

for item in accountsLatestState:
    businessOwnerFacebookId = item.get("business_owner_facebook_id")
    adAccountFacebookIds = list(set(item.get("ad_account_ids")))

    businessOwnerPermanentFacebookToken = BusinessOwnerTokenHelper(startup.Session).GetToken(businessOwnerFacebookId=businessOwnerFacebookId)

    facebookApiClient = BaseFacebookAdsApi(businessOwnerPermanentFacebookToken=businessOwnerPermanentFacebookToken, facebookConfig=startup.facebookConfig)

    insights_orchestrator = Orchestrator(facebookApiClient, mongoRepository)

    for adAccountFacebookId in adAccountFacebookIds:
        for level in levels:
            if level != Level.account:
                    print("..AD ACCOUNT: %s. LEVEL: %s. Started at: %s" % (adAccountFacebookId, level, datetime.now()))

                    insightsJobDefinition = syncInsightsJobsDefinitionsFactory.get(level)

                    config = OrchestratorRunConfig(business_owner_facebook_id=businessOwnerFacebookId,
                                                   account_id=adAccountFacebookId,
                                                   fields=insightsJobDefinition.fields,
                                                   level=level)


                    config.date_start = absolute_date_start.strftime("%Y-%m-%d")
                    config.date_stop = absolute_date_stop.strftime("%Y-%m-%d")

                    has_data = insights_orchestrator.check_data(run_config=config)

                    if has_data:
                        date_start = absolute_date_start
                        date_stop = date_start + timedelta(days=7)

                        while date_stop < datetime.now():
                            print("..Syncing insigths data for account: %s, level: %s, BREAKDOWN: NONE. Action BREAKDOWN: NONE. Between: %s and %s. Started at: %s" % (adAccountFacebookId.upper(),
                                                                                                                                                                       level.upper(),
                                                                                                                                                                       date_start.strftime("%Y-%m-%d"),
                                                                                                                                                                       date_stop.strftime("%Y-%m-%d"),
                                                                                                                                                                       datetime.now()))

                            config.breakdown = None
                            config.action_breakdown = None
                            config.date_start = date_start.strftime("%Y-%m-%d")
                            config.date_stop = date_stop.strftime("%Y-%m-%d")
                            config.collection_name = level + "-none-none"
                            config.time_increment = "1"

                            has_data = insights_orchestrator.run_sync_job(config, True)
                            if has_data or has_data is None:
                                for breakdown in insightsJobDefinition.breakdowns:
                                    print("..Syncing insights data for account: %s, level: %s, BREAKDOWN: %s. Action BREAKDOWN: NONE. Between: %s and %s.  Started at: %s" % (adAccountFacebookId.upper(),
                                                                                                                                                                              level.upper(),
                                                                                                                                                                              breakdown.Name.upper(),
                                                                                                                                                                              date_start.strftime("%Y-%m-%d"),
                                                                                                                                                                              date_stop.strftime("%Y-%m-%d"),
                                                                                                                                                                              datetime.now()))

                                    config.breakdown = breakdown
                                    config.action_breakdown = None
                                    config.collection_name = level + "-" + breakdown.Name + "-none"
                                    config.time_increment = "1"

                                    insights_orchestrator.run_sync_job(config, False)

                                for action_breakdown in insightsJobDefinition.action_breakdowns:
                                    print("Syncing insigths data for account: %s, level: %s, BREAKDOWN: NONE. Action BREAKDOWN: %s. Between: %s and %s. Started at: %s" % (adAccountFacebookId.upper(),
                                                                                                                                                                           level.upper(),
                                                                                                                                                                           date_start.strftime("%Y-%m-%d"),
                                                                                                                                                                           date_stop.strftime("%Y-%m-%d"),
                                                                                                                                                                           action_breakdown.Name.upper(),
                                                                                                                                                                           datetime.now()))

                                    config.breakdown = None
                                    config.action_breakdown = action_breakdown
                                    config.collection_name = level + "-none-" + action_breakdown.Name
                                    config.time_increment = "1"

                                    insights_orchestrator.run_sync_job(config, False)

                            date_start = date_stop
                            date_stop = date_start + timedelta(days=7)

                        print("...Finished syncing insigths data for account: %s, level: %s at: %s" % (adAccountFacebookId.upper(), level.upper(), datetime.now()))
                    else:
                        print("..Account %s has no data." % adAccountFacebookId.upper())

# TODO: Publish fanout message with new or updated structures

print('Finished syncing all add accounts at %s' % datetime.now())