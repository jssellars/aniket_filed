import copy
import typing
from datetime import datetime

from facebook_business.adobjects.adaccount import AdAccount

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookAudiences.Infrastructure.Domain.Audience import Audience
from FacebookAudiences.Infrastructure.Domain.AudienceStateEnum import AudienceStateEnum
from FacebookAudiences.Infrastructure.Domain.AudienceTypeEnum import AudienceTypeEnum
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPICustomAudienceDto import GraphAPICustomAudienceDto, \
    OperationStatus
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPICustomAudienceFields, \
    GraphAPISavedAudienceFields
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPISavedAudienceDto import GraphAPISavedAudienceDto
from FacebookAudiences.Infrastructure.GraphAPIMappings.GraphAPICustomAudienceMapping import \
    GraphAPICustomAudienceMapping
from FacebookAudiences.Infrastructure.GraphAPIMappings.GraphAPISavedAudienceMapping import \
    GraphAPISavedAudienceMapping


class GraphAPIAudiencesHandler:
    __datetime_format = "%Y-%m-%dT%H:%M:%S"

    @classmethod
    def get_audiences(cls,
                      permanent_token: typing.AnyStr = None,
                      account_id: typing.AnyStr = None,
                      startup: typing.Any = None) -> typing.Tuple[typing.List[Audience], typing.Any]:

        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(startup.facebook_config, permanent_token)

        #  get audiences
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
    def get_custom_audiences(cls, account_id: typing.AnyStr = None) -> typing.List[GraphAPICustomAudienceDto]:
        ad_account = AdAccount(fbid=account_id)
        custom_audiences = ad_account.get_custom_audiences(fields=GraphAPICustomAudienceFields.get_values())
        custom_audience_mapper = GraphAPICustomAudienceMapping(target=GraphAPICustomAudienceDto)
        custom_audiences = custom_audience_mapper.load(custom_audiences, many=True)

        return custom_audiences

    @classmethod
    def get_saved_audiences(cls, account_id: typing.AnyStr = None) -> typing.List[GraphAPISavedAudienceDto]:
        ad_account = AdAccount(fbid=account_id)
        saved_audiences = ad_account.get_saved_audiences(fields=GraphAPISavedAudienceFields.get_values())
        saved_audiences_mapper = GraphAPISavedAudienceMapping(target=GraphAPISavedAudienceDto)
        saved_audiences = saved_audiences_mapper.load(saved_audiences, many=True)

        return saved_audiences

    @classmethod
    def __timestamp_to_datetime(cls, timestamp: typing.Union[int, str] = None) -> typing.AnyStr:
        if isinstance(timestamp, int):
            return datetime.fromtimestamp(timestamp).strftime(cls.__datetime_format)
        else:
            return timestamp

    @classmethod
    def __map_delivery_status(cls, delivery_status: OperationStatus) -> typing.AnyStr:
        if delivery_status.code == 200:
            return AudienceStateEnum.ACTIVE.value
        else:
            return AudienceStateEnum.INACTIVE.value

    @classmethod
    def __map_custom_audience_subtype(cls, subtype: typing.AnyStr = None) -> typing.AnyStr:
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
        audience.audience_state = saved_audience.run_status

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
        audience.audience_state = cls.__map_delivery_status(custom_audience.delivery_status)

        last_updated = cls.__timestamp_to_datetime(custom_audience.time_updated)
        audience.last_updated = last_updated if last_updated else datetime.now().strftime(cls.__datetime_format)

        return audience
