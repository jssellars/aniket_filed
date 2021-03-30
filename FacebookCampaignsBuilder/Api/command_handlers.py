import logging
from typing import Any, Dict, Optional

from Core.facebook.sdk_adapter.smart_create import ad_builder
from Core.mongo_adapter import MongoOperator, MongoRepositoryBase
from Core.Tools.Misc.FiledAdFormatEnum import FiledAdFormatEnum
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from facebook_business.adobjects.adaccount import AdAccount
from FacebookCampaignsBuilder.Api import commands
from FacebookCampaignsBuilder.Api.startup import config
from FacebookCampaignsBuilder.Infrastructure.Mappings.PublishStatus import \
    PublishStatus
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


class AdPreview:
    @classmethod
    def handle(
        cls,
        command: commands.AdPreview = None,
        facebook_config: Any = None,
        permanent_token: str = None,
        uploaded_image: FileStorage = None,
    ) -> Optional[str]:
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

        ad_creative = None
        ad_account = AdAccount(fbid=command.account_id)
        page_ids = dict(
            facebook_page_id=command.page_facebook_id,
            instagram_page_id=command.instagram_facebook_id,
        )
        if command.ad_template["ad_format"] == FiledAdFormatEnum.IMAGE.value:
            ad_creative = ad_builder.build_image_ad_creative(
                page_ids, command.ad_template, ad_account, command.objective, uploaded_image
            )
        elif command.ad_template["ad_format"] == FiledAdFormatEnum.VIDEO.value:
            ad_creative = ad_builder.build_video_ad_creative(
                page_ids, command.ad_template, ad_account, command.objective
            )
        elif command.ad_template["ad_format"] == FiledAdFormatEnum.CAROUSEL.value:
            ad_creative = ad_builder.build_carousel_ad_creative(
                page_ids, command.ad_template, ad_account, command.objective
            )
        elif command.ad_template["ad_format"] == FiledAdFormatEnum.EXISTING_POST.value:
            ad_creative = ad_builder.build_existing_ad_creative(ad_account, command.ad_template["post_id"])

        params = {"ad_format": command.ad_format, "creative": ad_creative}
        ad_preview = ad_account.get_generate_previews(params=params)

        if ad_preview:
            return ad_preview[0].export_all_data()["body"].replace('scrolling="yes"', 'scrolling="no"')

        return None


class AudienceSize:
    @classmethod
    def handle(
        cls,
        permanent_token: str = None,
        account_id: str = None,
        audience_details: Dict = None,
    ):
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        try:
            account = AdAccount(account_id)
            response = account.get_delivery_estimate(fields=["estimate_mau"], params=audience_details)

        except Exception as e:
            raise e

        if isinstance(response, Exception):
            raise response

        audience_size_estimate = response[0].get("estimate_mau", None)
        return audience_size_estimate


class PublishProgress:
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )

    @staticmethod
    def get_publish_feedback(user_filed_id: int):
        date_key = "start_date"
        query = {"user_filed_id": {MongoOperator.EQUALS.value: user_filed_id}}
        sort_query = [(date_key, -1)]

        feedback_docs = PublishProgress.feedback_repository.get_sorted(query=query, sort_query=sort_query)
        if not feedback_docs:
            return

        feedback = feedback_docs[0]
        if feedback["publish_status"] != PublishStatus.IN_PROGRESS.value:
            PublishProgress.feedback_repository.delete_many({"user_filed_id": user_filed_id})

        feedback[date_key] = feedback[date_key].isoformat()
        feedback.pop("_id")

        return feedback
