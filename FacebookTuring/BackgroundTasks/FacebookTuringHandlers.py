import json

from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator
from FacebookTuring.BackgroundTasks.startup import fixtures
from FacebookTuring.Infrastructure.IntegrationEvents.CampaignCreatedEvent import CampaignCreatedEvent
from FacebookTuring.Infrastructure.IntegrationEvents.CampaignCreatedEventMapping import CampaignCreatedEventMapping
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


def turing_data_sync_handler(request_handler=None, message_body=None, config=None):
    # Initialize mongo repositories for accounts journal, insights and structures
    account_journal_repository = TuringAdAccountJournalRepository(config=config.mongo,
                                                                  database_name=config.mongo.accounts_journal_database_name,
                                                                  collection_name=config.mongo.accounts_journal_collection_name)
    insights_repository = TuringMongoRepository(config=config.mongo,
                                                database_name=config.mongo.insights_database_name)
    structures_repository = TuringMongoRepository(config=config.mongo,
                                                  database_name=config.mongo.structures_database_name)

    # Initialize orchestrator
    orchestrator = (Orchestrator().
                    set_account_journal_repository(account_journal_repository).
                    set_insights_repository(insights_repository).
                    set_structures_repository(structures_repository))

    # handle message
    (request_handler.
     set_mongo_repository(account_journal_repository).
     set_orchestrator(orchestrator).
     handle(message_body, config.days_to_sync))


def campaign_created_handler(request_handler=None, message_body=None, config=None):
    structures_repository = TuringMongoRepository(config=config.mongo,
                                                  database_name=config.mongo.structures_database_name)

    body = json.loads(message_body)
    mapper = CampaignCreatedEventMapping(target=CampaignCreatedEvent)
    message = mapper.load(body)

    # handle message
    (request_handler.
     set_repository(structures_repository).
     set_config(config).
     handle(message, fixtures))


FACEBOOK_TURING_HANDLERS = {
    RequestTypeEnum.BUSINESS_OWNER_UPDATE_EVENT.value: turing_data_sync_handler,
    RequestTypeEnum.CAMPAIGN_CREATED_EVENT.value: campaign_created_handler
}
