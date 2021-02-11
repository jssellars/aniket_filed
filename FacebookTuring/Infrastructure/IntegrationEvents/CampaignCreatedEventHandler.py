import logging
import typing
from datetime import datetime

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestSingleStructure import \
    GraphAPIRequestSingleStructure
from FacebookTuring.Infrastructure.IntegrationEvents.CampaignCreatedEvent import CampaignCreatedEvent
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields, StructureMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

logger = logging.getLogger(__name__)


class CampaignCreatedEventHandler:
    RATE_LIMIT_EXCEPTION_STATUS = 80004
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600
    __repository = None
    _config = None

    @classmethod
    def set_repository(cls, repository: TuringMongoRepository = None):
        cls.__repository = repository
        return cls

    @classmethod
    def set_config(cls, config=None):
        cls._config = config
        return cls

    @classmethod
    def handle(cls, message: CampaignCreatedEvent, fixtures: Fixtures):

        permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_id)

        # process message. sync every campaign, ad set, ad
        for campaign in message.campaign_tree:
            try:
                cls.__sync(
                    level=Level.CAMPAIGN,
                    account_id=message.account_id,
                    facebook_id=campaign.facebook_id,
                    business_owner_id=message.business_owner_id,
                    permanent_token=permanent_token,
                )
            except Exception as e:
                logger.exception(f"Failed to get campaign {campaign.facebook_id} || {repr(e)}")

            for adset in campaign.ad_sets:
                try:
                    cls.__sync(
                        level=Level.ADSET,
                        account_id=message.account_id,
                        facebook_id=adset.get("facebook_id"),
                        business_owner_id=message.business_owner_id,
                        permanent_token=permanent_token,
                    )
                except Exception as e:
                    logger.exception(f"Failed to get campaign {adset.facebook_id} || {repr(e)}")

                for ad in adset.get("ads", []):
                    try:
                        cls.__sync(
                            level=Level.AD,
                            account_id=message.account_id,
                            facebook_id=ad,
                            business_owner_id=message.business_owner_id,
                            permanent_token=permanent_token,
                        )
                    except Exception as e:
                        logger.exception(f"Failed to get campaign {ad} || {repr(e)}")

    @classmethod
    def __sync(
        cls,
        level: Level = None,
        account_id: typing.AnyStr = None,
        facebook_id: typing.AnyStr = None,
        business_owner_id: typing.AnyStr = None,
        permanent_token: typing.AnyStr = None,
    ) -> typing.NoReturn:

        # create an instance of the Graph API SDK. This is required to authenticate user requests to FB.
        _ = GraphAPISdkBase(cls._config.facebook, permanent_token)
        try:
            graph_api_client = GraphAPIClientBase(permanent_token)
            structure_fields = StructureFields.get(level.value)
            graph_api_client.config = cls.build_facebook_api_client_get_details_config(
                facebook_id=facebook_id,
                business_owner_permanent_token=permanent_token,
                fields=structure_fields.get_structure_fields(),
            )
            updated_structure, _ = graph_api_client.call_facebook()
            if isinstance(updated_structure, Exception):
                raise updated_structure

            # Map Facebook structure to domain model
            mapping = StructureMapping.get(level.value)
            updated_structure = mapping.load(updated_structure)
            updated_structure.last_updated_at = datetime.now()
            updated_structure.business_owner_facebook_id = business_owner_id
            updated_structure.account_id = account_id
        except Exception as e:
            raise e

        try:
            structure_id = getattr(
                updated_structure, LevelToFacebookIdKeyMapping.get_enum_by_name(Level(level).name).value
            )
            cls.__repository.add_structure(level=level, key_value=structure_id, document=updated_structure)
        except Exception as e:
            raise e

    @classmethod
    def build_facebook_api_client_get_details_config(
        cls, business_owner_permanent_token=None, facebook_id=None, fields=None
    ) -> GraphAPIClientBaseConfig:
        api_config = GraphAPIClientBaseConfig()
        api_config.try_partial_requests = False
        api_config.request = GraphAPIRequestSingleStructure(
            facebook_id=facebook_id, business_owner_permanent_token=business_owner_permanent_token, fields=fields
        )
        api_config.fields = fields
        return api_config
