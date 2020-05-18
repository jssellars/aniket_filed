import functools
import operator
import typing
from time import sleep

from facebook_business.exceptions import FacebookRequestError

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.Models.Field import Field
from FacebookTuring.BackgroundTasks.Startup import startup
from FacebookTuring.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.Mappings.StructureMapping import StructureFields, StructureMapping
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class StructuresSyncronizer:
    RATE_LIMIT_EXCEPTION_STATUS = 80004
    SLEEP_ON_RATE_LIMIT_EXCEPTION = 3600

    def __init__(self,
                 business_owner_id: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 level: Level = None):
        self.business_owner_id = business_owner_id
        self.account_id = account_id
        self.level = level

        self.__ad_account_id = "act_" + self.account_id
        self.__permanent_token = None
        self.__mongo_repository = None

    def run(self) -> typing.NoReturn:
        try:
            # get structures for ad account
            fields = StructureFields.get(self.level.value)

            # stop run if there are no available fields to sync for the desired level
            if not fields:
                return

            structures_response, _ = GraphAPIInsightsHandler.get_structures_base(permanent_token=self.permanent_token,
                                                                                 ad_account_id=self.__ad_account_id,
                                                                                 level=self.level.value,
                                                                                 fields=self.__get_fields(
                                                                                     fields.structure_fields))

            # map Facebook structure to domain model
            mapping = StructureMapping.get(self.level.value)
            structures = mapping.load(structures_response, many=True)

            # set business owner id
            structures = self.__set_business_owner_id(structures, self.business_owner_id)

            # insert structures
            self.__mongo_repository.add_structure_many(self.account_id, self.level, structures)
        except FacebookRequestError as fb_ex:
            if fb_ex.http_status() == self.RATE_LIMIT_EXCEPTION_STATUS:
                sleep(self.SLEEP_ON_RATE_LIMIT_EXCEPTION)
        except Exception as e:
            raise e

    def set_mongo_repository(self, mongo_repository: TuringMongoRepository = None) -> typing.Any:
        self.__mongo_repository = mongo_repository
        return self

    def close_database_connection(self):
        self.__mongo_repository.close()

    @property
    def permanent_token(self) -> typing.AnyStr:
        if self.__permanent_token is None:
            self.__permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
                self.business_owner_id)
        return self.__permanent_token

    @staticmethod
    def __get_fields(fields: typing.List[Field] = None) -> typing.List[typing.AnyStr]:
        fields = [field.facebook_fields for field in fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return fields

    @staticmethod
    def __set_business_owner_id(structures: typing.List[typing.Any] = None, business_owner_id: typing.AnyStr = None) -> \
            typing.List[typing.Any]:
        for index in range(len(structures)):
            structures[index].business_owner_facebook_id = business_owner_id
        return structures
