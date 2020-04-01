import asyncio
from copy import deepcopy

from facebook_business.adobjects.adreportrun import AdReportRun

from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestBase import HTTPRequestBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIGetHelper(HTTPRequestBase):

    _sleep_before_getting_data = 1
    _async_job_completed_percentage = 100
    _async_job_failed_status = 'Job Failed'
    limit = 100

    __report_run_id_key = "report_run_id"
    __fields_num = 10

    def _get_graph_api_base(self, config):
        try:
            response, summary = self.get(config.request.url)
        except Exception as e:
            # TODO: Log error
            raise Exception(e)

        return response, summary

    def _get_graph_api_base_async(self, config):
        try:
            ad_report = self.post(url=config.request.url)
        except Exception as e:
            # TODO: Log errors
            raise Exception(e)

        try:
            if self.__report_run_id_key in ad_report.keys():
                ad_report_response = AdReportRun(fbid=ad_report[self.__report_run_id_key])
                event_loop = asyncio.new_event_loop()
                task = event_loop.create_task(self._loop_graph_api_for_async_response(ad_report_response, config.async_trials))
                response = event_loop.run_until_complete(task)
            else:
                response = []
        except Exception as e:
            # TODO: Log errors
            raise Exception(e)

        return response

    def _get_partial_graph_api_base(self, config):
        if config.request is None:
            # TODO: Log error
            raise Exception('Missing Fields API request. Please provide an appropriate FB API request and try again.')

        try:
            partial_responses = []
            summary = []
            for partial_fields in self._get_fields_partitions(config.fields, config.required_field):
                config.request.modify_fields_and_params(partial_fields, config.params)
                partial_response, summary = self._get_graph_api_base(config)
                if not isinstance(partial_response, Exception) and partial_response:
                    partial_responses.append(deepcopy(partial_response))
                elif isinstance(partial_response, Exception):
                    # todo: log error
                    pass
            # Combine partial responses for different groups of fields into one response
            response = self._combine_partial_responses(partial_responses, config.required_field)
        except Exception as e:
            # TODO: Log error
            raise Exception(e)

        return response, summary

    #  ====== Helper methods ====== #
    async def _loop_graph_api_for_async_response(self, response, async_trials: int = None):
        """Helper method to continually probe FB async job report until completed or failure"""
        retry_num = 1

        response.api_get()  # Probe FB ad report

        while (response[AdReportRun.Field.async_percent_completion] < self._async_job_completed_percentage and response[AdReportRun.Field.async_status] != self._async_job_failed_status) and retry_num <= async_trials:
            await asyncio.sleep(1 ** retry_num)
            response.api_get()
            retry_num += 1

        # Wait before making request to get results to allow FB to send all data
        try:
            await asyncio.sleep(self._sleep_before_getting_data)
            async_job_response = response.get_result()
            if not isinstance(async_job_response, Exception):
                async_job_response = list(map(Tools.convert_to_json, async_job_response))
            else:
                # todo: log error
                pass
        except Exception as e:
            raise Exception(e)

        return async_job_response

    @staticmethod
    def sorted_zip_longest(l1, l2, key, fillvalue=None):
        if fillvalue is None:
            fillvalue = {}
        l1 = iter(sorted(l1, key=lambda x: x[key]))
        l2 = iter(sorted(l2, key=lambda x: x[key]))
        u = next(l1, None)
        v = next(l2, None)

        while (u is not None) or (v is not None):
            if u is None:
                yield fillvalue, v
                v = next(l2, None)
            elif v is None:
                yield u, fillvalue
                u = next(l1, None)
            elif u.get(key) == v.get(key):
                yield u, v
                u = next(l1, None)
                v = next(l2, None)
            elif u.get(key) < v.get(key):
                yield u, fillvalue
                u = next(l1, None)
            else:
                yield fillvalue, v
                v = next(l2, None)

    @staticmethod
    def _combine_partial_responses(partial_responses: list, required_field: str):
        if partial_responses and isinstance(partial_responses[0], list):
            response = partial_responses[0]
            partial_responses_num = len(partial_responses)

            for index in range(1, partial_responses_num):
                response = [{**u, **v} for u, v in GraphAPIGetHelper.sorted_zip_longest(response, partial_responses[index], key=required_field, fillvalue={})]

        else:
            response = partial_responses

        return response

    @staticmethod
    def _get_fields_partitions(fields: list, required_field: str = None):
        n = len(fields)
        indices = range(0, n, GraphAPIGetHelper.__fields_num)
        for index in indices:
            if required_field:
                yield list(set(fields[index:index + GraphAPIGetHelper.__fields_num] + [required_field]))
            else:
                yield list(set(fields[index:index + GraphAPIGetHelper.__fields_num]))

