from abc import ABC
from dataclasses import dataclass, field
from typing import Any, AnyStr, Dict, List, Optional

from marshmallow import EXCLUDE, fields, pre_load

from Core.mapper import MapperBase, MapperNestedField
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookCampaignsBuilder.Infrastructure.Mappings.PublishStatus import PublishStatus


@dataclass
class AddAdsetAdTree:
    facebook_id: AnyStr = None
    adsets: List[Dict] = field(default_factory=list)
    ads: List[AnyStr] = field(default_factory=list)


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
class EditedStructureTree:
    facebook_id: AnyStr = None
    ad_sets: List[AdSetTree] = field(default_factory=list)


@dataclass
class CampaignCreatedEvent:
    message_type = "CampaignCreatedEvent"
    business_owner_id: AnyStr = None
    account_id: AnyStr = None
    campaign_tree: List[CampaignTree] = field(default_factory=list)


@dataclass
class StructureEditedEvent:
    message_type = "StructureEditedEvent"
    business_owner_id: AnyStr = None
    account_id: AnyStr = None
    structure_tree: List[Dict] = field(default_factory=list)


@dataclass
class AddAdsetAdEvent:
    message_type = "AddAdsetAdEvent"
    business_owner_id: AnyStr = None
    account_id: AnyStr = None
    structure_tree: List[Dict] = field(default_factory=list)


class CampaignCreatedEventMapping(MapperBase):
    business_owner_id = fields.String()
    account_id = fields.String()
    campaign_tree = MapperNestedField(target=CampaignTree, many=True)

    @pre_load
    def convert(self, data: Any, **kwargs):
        if isinstance(data, list):
            data = {"campaign_tree": data}
        return data

    class Meta:
        unknown = EXCLUDE


class StructureEditedEventMapping(MapperBase):
    business_owner_id = fields.String()
    account_id = fields.String()
    structure_tree = MapperNestedField(target=EditedStructureTree, many=True)

    @pre_load
    def convert(self, data: Any, **kwargs):
        if isinstance(data, list):
            data = {"edited_structure_tree": data}
        return data

    class Meta:
        unknown = EXCLUDE


class AddAdsetAdEventMapping(MapperBase):
    business_owner_id = fields.String()
    account_id = fields.String()
    structure_tree = MapperNestedField(target=AddAdsetAdTree, many=True)

    @pre_load
    def convert(self, data: Any, **kwargs):
        if isinstance(data, list):
            data = {"edited_structure_tree": data}
        return data

    class Meta:
        unknown = EXCLUDE


class RequestTypeEnum(EnumerationBase):
    SMART_CREATE_PUBLISH_REQUEST = "SmartCreatePublishRequestEvent"
    SMART_EDIT_PUBLISH_REQUEST = "SmartEditPublishRequestEvent"
    AAA_PUBLISH_REQUEST = "AddAdsetAdPublishRequestEvent"


class ResponseTypeEnum(EnumerationBase):
    SMART_CREATE_PUBLISH_RESPONSE = "SmartCreatePublishResponseEvent"
    SMART_EDIT_PUBLISH_RESPONSE = "SmartEditPublishResponseEvent"
    AAA_PUBLISH_RESPONSE = "AddAdsetAdPublishResponseEvent"


class PublishResponseEvent(ABC):
    """
    Abstract Base Class for the below:
    SmartCreatePublishResponseEvent,
    SmartEditPublishResponseEvent,
    AddAdsetAdPublishResponseEvent
    or any future Publish Response Event to RabbitMQ dataclasses extend
    to enforce type checking and type hints
    """

    pass


@dataclass
class SmartCreatePublishResponseEvent(PublishResponseEvent):
    template_id: int
    message_type: str = ResponseTypeEnum.SMART_CREATE_PUBLISH_RESPONSE.value
    publish_status_id: int = PublishStatus.SUCCESS.value


@dataclass
class SmartEditPublishResponseEvent(PublishResponseEvent):
    message_type: str = ResponseTypeEnum.SMART_EDIT_PUBLISH_RESPONSE.value
    publish_status_id: int = PublishStatus.SUCCESS.value


@dataclass
class AddAdsetAdPublishResponseEvent(PublishResponseEvent):
    message_type: str = ResponseTypeEnum.AAA_PUBLISH_RESPONSE.value
    publish_status_id: int = PublishStatus.SUCCESS.value


@dataclass
class PublishAddAdsetAdEvent:
    message_type = RequestTypeEnum.AAA_PUBLISH_REQUEST.value
    business_owner_facebook_id: str
    ad_account_id: str
    parent_level: str
    child_level: str
    user_filed_id: str
    parent_ids: List[str]
    child_ids: List[str]
    adsets: Optional[List[Dict]] = field(default_factory=list)
    ads: Optional[List[Dict]] = field(default_factory=list)


@dataclass
class PublishSmartEditEvent:
    message_type = RequestTypeEnum.SMART_EDIT_PUBLISH_REQUEST.value
    business_owner_facebook_id: str
    ad_account_id: str
    user_filed_id: str
    campaigns: Optional[List[Dict]] = field(default_factory=list)
    adsets: Optional[List[Dict]] = field(default_factory=list)
    ads: Optional[List[Dict]] = field(default_factory=list)
