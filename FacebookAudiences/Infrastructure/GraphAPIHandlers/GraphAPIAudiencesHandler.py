import copy
from datetime import datetime
from typing import Any, List, Tuple, Union

from Core.settings_models import Model
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.adaccount import AdAccount
from FacebookAudiences.Infrastructure.Domain.Audience import Audience
from FacebookAudiences.Infrastructure.Domain.AudienceStateEnum import AudienceStateEnum
from FacebookAudiences.Infrastructure.Domain.AudienceTypeEnum import AudienceTypeEnum
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPICustomAudienceDto import (
    GraphAPICustomAudienceDto,
    OperationStatus,
)
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIFields import (
    GraphAPICustomAudienceFields,
    GraphAPISavedAudienceFields,
)
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPISavedAudienceDto import GraphAPISavedAudienceDto
from FacebookAudiences.Infrastructure.GraphAPIMappings.GraphAPICustomAudienceMapping import (
    GraphAPICustomAudienceMapping,
)
from FacebookAudiences.Infrastructure.GraphAPIMappings.GraphAPISavedAudienceMapping import GraphAPISavedAudienceMapping


class GraphAPIAudiencesHandler:
    __datetime_format = "%Y-%m-%dT%H:%M:%S"

    @classmethod
    def get_audiences(
        cls, permanent_token: str = None, account_id: str = None, config: Model = None
    ) -> Tuple[List[Audience], Any]:

        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        # get audiences
        audiences = []
        errors = []
        try:
            custom_audiences = cls.get_custom_audiences(account_id=account_id)
            mapped_audiences = [cls.__map_custom_audience(audience) for audience in custom_audiences]
            audiences.extend(mapped_audiences)
        except Exception as e:
            errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

        try:
            saved_audiences = cls.get_saved_audiences(account_id=account_id)
            mapped_audiences = [cls.__map_saved_audience(audience) for audience in saved_audiences]
            audiences.extend(mapped_audiences)
        except Exception as e:
            errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

        return audiences, errors

    @classmethod
    def get_custom_audiences(cls, account_id: str = None) -> List[GraphAPICustomAudienceDto]:
        ad_account = AdAccount(fbid=account_id)
        custom_audiences = ad_account.get_custom_audiences(fields=GraphAPICustomAudienceFields.get_values())
        custom_audience_mapper = GraphAPICustomAudienceMapping(target=GraphAPICustomAudienceDto)
        custom_audiences = custom_audience_mapper.load(custom_audiences, many=True)

        return custom_audiences

    @classmethod
    def get_saved_audiences(cls, account_id: str = None) -> List[GraphAPISavedAudienceDto]:
        ad_account = AdAccount(fbid=account_id)
        saved_audiences = ad_account.get_saved_audiences(fields=GraphAPISavedAudienceFields.get_values())
        saved_audiences_mapper = GraphAPISavedAudienceMapping(target=GraphAPISavedAudienceDto)
        saved_audiences = saved_audiences_mapper.load(saved_audiences, many=True)

        return saved_audiences

    @classmethod
    def __timestamp_to_datetime(cls, timestamp: Union[int, str] = None) -> str:
        if isinstance(timestamp, int):
            return datetime.fromtimestamp(timestamp).strftime(cls.__datetime_format)
        else:
            return timestamp

    @classmethod
    def __map_delivery_status(cls, delivery_status: OperationStatus) -> str:
        if delivery_status.code == 200:
            return AudienceStateEnum.ACTIVE.value
        else:
            return AudienceStateEnum.INACTIVE.value

    @classmethod
    def __map_custom_audience_subtype(cls, subtype: str = None) -> str:
        if subtype == AudienceTypeEnum.LOOKALIKE.value:
            return AudienceTypeEnum.LOOKALIKE.value
        else:
            return AudienceTypeEnum.CUSTOM.value

    @classmethod
    def __map_saved_audience(cls, saved_audience: GraphAPISavedAudienceDto) -> Audience:
        audience = Audience()
        audience.facebook_id = saved_audience.id
        audience.name = saved_audience.name
        audience.type = AudienceTypeEnum.SAVED.value
        audience.date_created = saved_audience.time_created
        audience.size = saved_audience.approximate_count
        audience.details = copy.deepcopy(object_to_json(saved_audience))
        audience.state = AudienceStateEnum[saved_audience.run_status].value
        audience.locations = saved_audience.locations
        audience.languages = saved_audience.languages
        audience.interests = saved_audience.interests
        audience.excluded_interests = saved_audience.excluded_interests
        audience.narrow_interests = saved_audience.narrow_interests
        audience.age_range = saved_audience.age_range
        audience.gender = saved_audience.gender
        audience.custom_audiences = audience.included_custom_audiences = saved_audience.custom_audiences
        audience.excluded_custom_audiences = saved_audience.excluded_custom_audiences

        last_updated = cls.__timestamp_to_datetime(saved_audience.time_updated)
        audience.last_updated = last_updated if last_updated else datetime.now().strftime(cls.__datetime_format)

        return audience

    @classmethod
    def __map_custom_audience(cls, custom_audience: GraphAPICustomAudienceDto) -> Audience:
        audience = Audience()
        audience.facebook_id = custom_audience.id
        audience.name = custom_audience.name
        audience.type = cls.__map_custom_audience_subtype(custom_audience.subtype)
        audience.subtype = custom_audience.subtype
        audience.source = custom_audience.data_source.type if custom_audience.data_source else None
        audience.date_created = cls.__timestamp_to_datetime(custom_audience.time_created)
        audience.size = custom_audience.approximate_count
        audience.details = copy.deepcopy(object_to_json(custom_audience))
        audience.pixel_id = custom_audience.pixel_id
        audience.state = cls.__map_delivery_status(custom_audience.delivery_status)

        last_updated = cls.__timestamp_to_datetime(custom_audience.time_updated)
        audience.last_updated = last_updated if last_updated else datetime.now().strftime(cls.__datetime_format)

        return audience
