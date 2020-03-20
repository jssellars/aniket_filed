from operator import getitem, setitem

import typing

from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Turing.BackgroundTasks.Orchestrators.OrchestratorRunConfig import OrchestratorRunConfig
from Turing.Infrastructure.GraphAPIHandlers.GraphAPIInsightsHandler import GraphAPIInsightsHandler
from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata


class Orchestrator:

    def __init__(self, mongo_repository: MongoRepositoryBase = None, mapper: typing.Any = None):
        self.mongo_repository = mongo_repository
        self.mapper = mapper

    def run_sync_job(self, run_config: OrchestratorRunConfig = None) -> typing.NoReturn:
        if run_config.check_has_data:
            has_data = self.check_data(run_config)
            if not has_data:
                return False

        try:
            response = GraphAPIInsightsHandler.get_insights(permanent_token=run_config.permanent_token,
                                                            level=run_config.level,
                                                            ad_account_id=run_config.account_id,
                                                            fields=run_config.fields,
                                                            parameters=run_config.params,
                                                            structure_fields=run_config.structure_fields,
                                                            requested_fields=run_config.requested_fields)

            account_id = run_config.account_id.split("_")[1]
            response = self.__add_account_id_if_missing(response, account_id)

            if run_config.structures_sync:
                response = self.mapper.load(response, many=True)
            self.mongo_repository.collection = run_config.collection_name
            self.mongo_repository.add_many(response)
        except Exception as e:
            # TODO: log exception
            print(e)

    @staticmethod
    def __add_account_id_if_missing(response: typing.List[typing.Dict], account_id: typing.AnyStr) -> typing.List[typing.Dict]:
        if response and not getitem(response[0], FacebookFieldsMetadata.ad_account_id.name):
            [setitem(response[index], FacebookFieldsMetadata.ad_account_id.name, account_id) for index in range(len(response))]

        return response

    @staticmethod
    def check_data(run_config: OrchestratorRunConfig) -> bool:
        try:
            response = GraphAPIInsightsHandler.get_insights(permanent_token=run_config.permanent_token,
                                                            level=run_config.level,
                                                            ad_account_id=run_config.account_id,
                                                            fields=run_config.fields,
                                                            parameters=run_config.params,
                                                            structure_fields=run_config.structure_fields,
                                                            requested_fields=run_config.requested_fields)
            return True if response else False
        except Exception as e:
            # TODO: log exception
            print(e)

