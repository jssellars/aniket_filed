import logging
import typing
from ast import parse
from datetime import datetime
from typing import List

from bson import BSON

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.StructureStatusEnum import StructureStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from FacebookTuring.BackgroundTasks.Orchestrators.StructuresSyncronizer import StructuresSyncronizer
from FacebookTuring.BackgroundTasks.startup import config, fixtures
from FacebookTuring.BackgroundTasks.SynchronizerConfig import SynchronizerConfigRuntime, SynchronizerConfigStatic
from FacebookTuring.Infrastructure.Domain.AdAccountSyncStatusEnum import AdAccountSyncStatusEnum
from FacebookTuring.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import (
    FacebookTuringDataSyncCompletedEvent,
    UpdatedBusinessOwnersDetails,
)
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import UserTypeEnum
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

logger = logging.getLogger(__name__)

DAYS_UNTIL_OBSOLETE = 61
USER_CONFIGS_BY_TYPE = {
    UserTypeEnum.FREEMIUM: SynchronizerConfigStatic(
        levels=[Level.CAMPAIGN],
    ),
    UserTypeEnum.PAYED: SynchronizerConfigStatic(
        levels=[Level.ADSET, Level.CAMPAIGN, Level.AD],
    ),
}


def sync(
    account_journal_repository: TuringAdAccountJournalRepository = None,
    business_owner_details: typing.List[typing.Dict] = None,
    user_type: UserTypeEnum = None,
    permanent_token: str = None,
) -> None:
    user_config_static = USER_CONFIGS_BY_TYPE.get(user_type, USER_CONFIGS_BY_TYPE[UserTypeEnum.PAYED])
    user_config_static.account_journal_repository = account_journal_repository

    _sequantial_sync(business_owner_details, user_config_static, permanent_token)


def _sequantial_sync(business_owner_details: List, user_config_static: SynchronizerConfigStatic, permanent_token: str):
    for entry in business_owner_details:
        sync_one_ad_account_structures(entry, user_config_static, permanent_token)
        _publish_business_owner_synced_event(
            entry[FacebookMiscFields.business_owner_id], entry[FacebookMiscFields.account_id]
        )
        user_config_static.account_journal_repository.update_last_sync_time_by_account_id(
            entry[FacebookMiscFields.account_id]
        )


def sync_one_ad_account_structures(entry, user_config_static: SynchronizerConfigStatic, permanent_token: str):
    last_synced_on = entry[FacebookMiscFields.last_synced_on]
    if isinstance(last_synced_on, str):
        last_synced_on = parse(last_synced_on)

    now = datetime.now().date()
    if last_synced_on.date() < now:
        user_config_runtime = SynchronizerConfigRuntime(
            business_owner_id=entry[FacebookMiscFields.business_owner_id],
            account_id=entry[FacebookMiscFields.account_id],
            date_start=last_synced_on,
        )

        try:

            user_config_static.account_journal_repository.change_account_structures_sync_status(
                user_config_runtime.account_id, AdAccountSyncStatusEnum.PENDING, start_date=datetime.now()
            )
            GraphAPISdkBase(config.facebook, permanent_token)
            _sync_structures(user_config_static=user_config_static, user_config_runtime=user_config_runtime)

        except Exception as e:
            logger.exception(
                f"Failed sync data for business owner: {entry[FacebookMiscFields.business_owner_id]}"
                f" and ad account: {entry[FacebookMiscFields.account_id]} || {repr(e)}"
            )
            user_config_static.account_journal_repository.change_account_structures_sync_status(
                user_config_runtime.account_id, AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS, start_date=datetime.now()
            )


def _sync_structures(
    user_config_static: SynchronizerConfigStatic, user_config_runtime: SynchronizerConfigRuntime
) -> None:
    user_config_static.account_journal_repository.change_account_structures_sync_status(
        user_config_runtime.account_id, AdAccountSyncStatusEnum.IN_PROGRESS, start_date=datetime.now()
    )
    has_errors = False

    for level in user_config_static.levels:
        synchronizer = StructuresSyncronizer(
            business_owner_id=user_config_runtime.business_owner_id,
            account_id=user_config_runtime.account_id,
            level=level,
        )
        try:

            (synchronizer.run())
        except Exception as e:
            logger.exception(
                f"Failed sync structures for business owner: {user_config_runtime.business_owner_id}"
                f" and ad account: {user_config_runtime.account_id} || {repr(e)}"
            )
            has_errors = True

    # mark campaigns and adsets as completed based on the end time value
    try:
        mark_structures_as_completed(account_id=user_config_runtime.account_id)
    except Exception as e:
        logger.exception(
            f"Failed updating completed structure ids for business owner: {user_config_runtime.business_owner_id}"
            f" and ad account: {user_config_runtime.account_id} || {repr(e)}"
        )
        has_errors = True

    sync_status = AdAccountSyncStatusEnum.COMPLETED_WITH_ERRORS if has_errors else AdAccountSyncStatusEnum.COMPLETED

    user_config_static.account_journal_repository.change_account_structures_sync_status(
        user_config_runtime.account_id, sync_status, end_date=datetime.now()
    )


def mark_structures_as_completed(account_id: str = None) -> None:
    structures_repository = TuringMongoRepository(
        config=config.mongo, database_name=config.mongo.structures_database_name
    )

    campaigns = structures_repository.get_campaigns_by_ad_account(account_id)
    campaign_ids = [campaign[LevelToFacebookIdKeyMapping.CAMPAIGN.value] for campaign in campaigns]
    adsets = structures_repository.get_adsets_by_campaign_id(campaign_ids)
    completed_campaigns, completed_adsets = mark_completed_campaigns_and_adsets(campaigns, adsets)

    update_status_for_completed_structures(
        structures_repository=structures_repository,
        completed_structures=completed_campaigns,
        structure_key=LevelToFacebookIdKeyMapping.CAMPAIGN.value,
        level=Level.CAMPAIGN.value,
    )

    update_status_for_completed_structures(
        structures_repository=structures_repository,
        completed_structures=completed_adsets,
        structure_key=LevelToFacebookIdKeyMapping.ADSET.value,
        level=Level.ADSET.value,
    )


def update_status_for_completed_structures(
    structures_repository: TuringMongoRepository = None,
    completed_structures: typing.List = None,
    structure_key: str = None,
    level: str = None,
):
    completed_structure_ids = [
        structure[structure_key]
        for structure in completed_structures
        if structure[FacebookMiscFields.status] == StructureStatusEnum.COMPLETED.value
    ]

    structures_repository.collection = level
    structures_repository.update_structure_status(
        structure_key=structure_key,
        structure_ids=completed_structure_ids,
        status_key=FacebookMiscFields.status,
        status_value=StructureStatusEnum.COMPLETED.value,
    )


def mark_completed_campaigns_and_adsets(
    campaigns: typing.List[typing.Dict] = None, adsets: typing.List[typing.Dict] = None
) -> typing.Tuple[typing.List[typing.Dict], typing.List[typing.Dict]]:
    for index in range(len(campaigns)):
        campaign_id = campaigns[index][LevelToFacebookIdKeyMapping.CAMPAIGN.value]
        campaign_adsets = [
            adset for adset in adsets if adset[LevelToFacebookIdKeyMapping.CAMPAIGN.value] == campaign_id
        ]

        completed_adsets = mark_completed_adset(campaign_adsets)
        if completed_adsets == len(campaign_adsets):
            campaigns[index][FacebookMiscFields.status] = StructureStatusEnum.COMPLETED.value

        campaigns[index][FacebookMiscFields.details] = BSON.encode(campaigns[index][FacebookMiscFields.details])

    for index in range(len(adsets)):
        adsets[index][FacebookMiscFields.details] = BSON.encode(adsets[index][FacebookMiscFields.details])

    return campaigns, adsets


def mark_completed_adset(adsets: typing.List[typing.Dict] = None) -> int:
    completed_adsets = 0
    for adset in adsets:
        end_time = adset.get(FacebookMiscFields.end_time)
        if end_time:
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S%z")
            now = datetime.now(end_time.tzinfo)
            if end_time < now:
                adset[FacebookMiscFields.status] = StructureStatusEnum.COMPLETED.value
                completed_adsets += 1
    return completed_adsets


def _publish_business_owner_synced_event(business_owner_id: str, ad_account_id: str) -> None:
    business_owner_updated_details = UpdatedBusinessOwnersDetails(
        business_owner_facebook_id=business_owner_id, ad_account_ids=[ad_account_id]
    )
    business_owner_synced_event = FacebookTuringDataSyncCompletedEvent(business_owners=[business_owner_updated_details])
    try:
        rabbitmq_adapter = fixtures.rabbitmq_adapter
        rabbitmq_adapter.publish(business_owner_synced_event)
        logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(business_owner_synced_event)})
    except Exception as e:
        logger.exception(f"{business_owner_synced_event.message_type} || {repr(e)}")
