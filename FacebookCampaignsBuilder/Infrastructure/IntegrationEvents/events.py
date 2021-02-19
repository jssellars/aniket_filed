from dataclasses import dataclass, field
from typing import Any, AnyStr, List

from Core.mapper import MapperBase, MapperNestedField
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookCampaignsBuilder.Infrastructure.Mappings.PublishStatus import \
    PublishStatus
from marshmallow import EXCLUDE, fields, pre_load


@dataclass
class AdSetTree:
    facebook_id: AnyStr = None
    ads: List[AnyStr] = field(default_factory=list)


@dataclass
class CampaignTree:
    facebook_id: AnyStr = None
    name: AnyStr = None
    ad_sets: List[AdSetTree] = field(default_factory=list)


@dataclass
class CampaignCreatedEvent:
    message_type = "CampaignCreatedEvent"
    business_owner_id: AnyStr = None
    account_id: AnyStr = None
    campaign_tree: List[CampaignTree] = field(default_factory=list)


class CampaignCreatedEventMapping(MapperBase):
    business_owner_id = fields.String()
    account_id = fields.String()
    campaign_tree = MapperNestedField(target=CampaignTree, many=True)

    @pre_load
    def convert(self, data: Any, **kwargs):
        if isinstance(data, list):
            data = {
                'campaign_tree': data
            }
        return data

    class Meta:
        unknown = EXCLUDE


class RequestTypeEnum(EnumerationBase):
    SMART_CREATE_PUBLISH_REQUEST = "SmartCreatePublishRequestEvent"


class ResponseTypeEnum(EnumerationBase):
    SMART_CREATE_PUBLISH_RESPONSE = "SmartCreatePublishResponseEvent"


@dataclass
class SmartCreatePublishResponseEvent:
    template_id: int
    message_type: str = ResponseTypeEnum.SMART_CREATE_PUBLISH_RESPONSE.value
    publish_status_id: int = PublishStatus.SUCCESS.value
