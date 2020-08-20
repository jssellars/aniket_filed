import json

from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator
from FacebookTuring.Infrastructure.IntegrationEvents.CampaignCreatedEvent import CampaignCreatedEvent
from FacebookTuring.Infrastructure.IntegrationEvents.CampaignCreatedEventMapping import CampaignCreatedEventMapping
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


def turing_data_sync_handler(request_handler=None, message_body=None, startup=None, logger=None, rabbit_logger=None):
    #  Initialize mongo repositories for accounts journal, insights and structures
    account_journal_repository = TuringAdAccountJournalRepository(config=startup.mongo_config,
                                                                  database_name=startup.mongo_config.accounts_journal_database_name,
                                                                  collection_name=startup.mongo_config.accounts_journal_collection_name,
                                                                  logger=logger)
    insights_repository = TuringMongoRepository(config=startup.mongo_config,
                                                database_name=startup.mongo_config.insights_database_name,
                                                logger=logger)
    structures_repository = TuringMongoRepository(config=startup.mongo_config,
                                                  database_name=startup.mongo_config.structures_database_name,
                                                  logger=logger)

    #  initialize orchestrator
    orchestrator = (Orchestrator().
                    set_account_journal_repository(account_journal_repository).
                    set_insights_repository(insights_repository).
                    set_structures_repository(structures_repository).
                    set_logger(logger).
                    set_rabbit_logger(rabbit_logger))

    # handle message
    (request_handler.
     set_mongo_repository(account_journal_repository).
     set_orchestrator(orchestrator).
     set_logger(logger).
     handle(message_body, startup.days_to_sync))


def campaign_created_handler(request_handler=None, message_body=None, startup=None, logger=None, rabbit_logger=None):
    structures_repository = TuringMongoRepository(config=startup.mongo_config,
                                                  database_name=startup.mongo_config.structures_database_name,
                                                  logger=logger)

    body = json.loads(message_body)
    mapper = CampaignCreatedEventMapping(target=CampaignCreatedEvent)
    message = mapper.load(body)

    # handle message
    (request_handler.
     set_repository(structures_repository).
     set_startup(startup).
     set_logger(logger).
     handle(message))


FACEBOOK_TURING_HANDLERS = {
    RequestTypeEnum.BUSINESS_OWNER_UPDATE_EVENT.value: turing_data_sync_handler,
    RequestTypeEnum.CAMPAIGN_CREATED_EVENT.value: campaign_created_handler
}
