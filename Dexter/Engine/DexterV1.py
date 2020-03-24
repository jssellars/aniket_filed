import logging
import threading

from Algorithms.Models.BusinessOwner import BusinessOwner
from Algorithms.Models.Types.Seeding import TypesSeeder
from Algorithms.Tools.RemoveActorPrefix import remove_actors_prefix
from Algorithms.Tools.TimeInterval import TimeInterval
from Infrastructure.Mongo.Mongo import MongoMediator
from Infrastructure.Rabbit.RabbitMQMediator import RabbitMqMediator
from MasterWorker import MasterWorker
from Algorithms.Tools.Columns import ChannelEnum
rabbit_mediator = RabbitMqMediator()


def synchronize_callback(ch, method, properties, body):
    try:

        logging.info('In synchronize_callback')
        print(f"body : {body}")
        print(f"properties: {properties.type}")
        logging.info(f"Received Message: {body}")
        message_type = properties.type

        # TODO: Get account ids from andrei. this is also a mock
        # TODO: this his dataclass, instantiate this with a mapper
        business_owners_raw_data = [
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

        business_owners_processed_data = []

        for business_owner in business_owners_raw_data:
            business_owners_processed_data.append(BusinessOwner(business_owner_id=business_owner['business_owner_facebook_id'],
                                                                ad_account_ids=remove_actors_prefix(business_owner['ad_account_ids'])
                                                                ))

        # TODO: The following line is a mock, due to the fact that it comes from a test_message
        if message_type == 'TuringSyncCompletedEvent':

            # TODO: check to see if we should recommend
            # TODO: make method for this, and there should be the logic
            should_recommend = True

            if should_recommend:

                for business_owner in business_owners_processed_data:
                    business_owner_thread = threading.Thread(target=MasterWorker.start_dexter_for_business_owner, args=(business_owner, ChannelEnum.FACEBOOK))
                    business_owner_thread.start()
                    # MasterWorker.start_dexter_for_business_owner(business_owner, channel=ChannelEnum.FACEBOOK)

    except Exception as exc:
        logging.exception(exc)


def configLogger():
    logging.basicConfig(
        filename='dexter.log',
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


configLogger()


# This function exists for test purposes only
# ShouldSync flag true = will send a message that would cause the database to be updated
#                 false = no new data will enter Dexter 
def SendTestMessages(should_sync=False):
    # ad_accounts = ["act_273538789947186", "act_1726846407528996", "act_306350493457114", "act_336659300318517", "act_62854450" ]
    ad_accounts = ["act_62854450"]

    if should_sync:
        date_ranges = [TimeInterval("2019-06-06", "2020-06-06")]
    else:
        date_ranges = [TimeInterval("2020-03-03", "2020-03-04")]

    for account in ad_accounts:
        for date_range in date_ranges:
            rabbit_mediator.send_test_messages(1, date_range, account)


try:
    # FLAGS
    # Mark this flag true if you want to re-seed optimization types at program start
    shouldSeed = False

    # Optimizations Seeding
    if shouldSeed:
        TypesSeeder.PushSeeds()

    # #Mark this flag true if you want to re-seed campaign goal definitions
    # shouldSeedGoals = False
    mongoMediator = MongoMediator()
    # expandedTypes = mongoMediator.get_expanded_types()

    # interTypes = list(expandedTypes)
    # budgetTypes = [interType for interType in interTypes if interType.name == 'Budget']

    # This will be fetched from campaigninsights message
    logging.info('Starting main flow')

    # Goals Seeding
    # if shouldSeedGoals:
    #     seed_goals()

    SendTestMessages(should_sync=False)

    # start listening for messages 
    rabbit_mediator.ListenForMessages(callback=synchronize_callback)

except Exception as e:
    logging.critical('Critical flow error!')
    logging.exception(e)

finally:
    logging.info('exiting main flow')
