import asyncio
from collections import ChainMap
from copy import deepcopy
from queue import Queue
from threading import Thread
from typing import List, Dict

from facebook_business.adobjects.adreportrun import AdReportRun

from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestBase import HTTPRequestBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIGetHelper(HTTPRequestBase):
    _sleep_before_getting_data = 1
    _async_job_completed_percentage = 100
    _async_job_failed_status = 'Job Failed'

    __report_run_id_key = "report_run_id"
    __fields_num = 8

    def _get_graph_api_base(self, config):
        try:
            response, summary = self.get(config.request.url)
        except Exception as e:
            raise e

        return response, summary

    def _get_graph_api_base_async(self, config):
        try:
            ad_report = self.post(url=config.request.url)
        except Exception as e:
            raise e

        try:
            if self.__report_run_id_key in ad_report.keys():
                ad_report_response = AdReportRun(fbid=ad_report[self.__report_run_id_key])
                event_loop = asyncio.new_event_loop()
                task = event_loop.create_task(
                    self._loop_graph_api_for_async_response(ad_report_response, config.async_trials)
                )
                response = event_loop.run_until_complete(task)
            else:
                response = []
        except Exception as e:
            raise e

        return response

    def _get_partial_graph_api_base(self, config):
        if config.request is None:
            raise Exception("Missing Fields API request. Please provide an appropriate FB API request and try again.")

        try:
            partial_responses = []
            summary = []
            workers = []
            queue = Queue()

            for partial_fields in self._get_fields_partitions(config.fields, config.required_field):
                config.request.modify_fields_and_params(partial_fields, config.params)

                worker_thread = Thread(
                    target=lambda q, arg1: q.put(self._get_graph_api_base(arg1)), args=(queue, deepcopy(config))
                )
                workers.append(worker_thread)

            # Combine partial responses for different groups of fields into one response
            for thread in workers:
                thread.start()

            for thread in workers:
                thread.join()

            while not queue.empty():
                partial_response, summary = queue.get()
                if not isinstance(partial_response, Exception) and partial_response:
                    partial_responses.append(deepcopy(partial_response))
                elif isinstance(partial_response, Exception):
                    raise partial_response

            response = self._combine_partial_responses(partial_responses, config.required_field)
        except Exception as e:
            raise e

        return response, summary

    def _get_insights_page(self, config, cursor_link=None):
        if config.request is None:
            raise Exception('Missing Fields API request. Please provide an appropriate FB API request and try again.')

        next_page_cursor = None
        summary = []

        try:
            partial_responses = []
            summary_responses = []
            workers = []
            queue = Queue()

            # TODO: remove partial fields logic after confirming calls go through
            for partial_fields in self._get_fields_partitions(config.fields, config.required_field):
                config.request.modify_fields_and_params(partial_fields, config.params, config.page_size)

                worker_thread = Thread(target=lambda q, arg1: q.put(self.get_page(arg1)),
                                       args=(queue, deepcopy(config.request.url)))
                workers.append(worker_thread)

            # Combine partial responses for different groups of fields into one response
            for thread in workers:
                thread.start()

            for thread in workers:
                thread.join()

            while not queue.empty():
                partial_response, next_page_cursor, summary_response = queue.get()
                if not isinstance(partial_response, Exception) and partial_response:
                    partial_responses.append(deepcopy(partial_response))
                elif isinstance(partial_response, Exception):
                    raise partial_response

                if not isinstance(summary_response, Exception) and summary_response:
                    summary_responses.append(deepcopy(summary_response))

            response = self._combine_partial_responses(partial_responses, config.required_field)
            summary = dict(ChainMap(*summary_responses))
        except Exception as e:
            raise e

        return response, next_page_cursor, summary

    #  ====== Helper methods ====== #
    async def _loop_graph_api_for_async_response(self, response, async_trials: int = None):
        """Helper method to continually probe FB async job report until completed or failure"""
        retry_num = 1

        response.api_get()  # Probe FB ad report

        while (
            response[AdReportRun.Field.async_percent_completion] < self._async_job_completed_percentage
            and response[AdReportRun.Field.async_status] != self._async_job_failed_status
        ) and retry_num <= async_trials:
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
        l1 = iter(sorted(l1, key=lambda x: x.get(key)))
        l2 = iter(sorted(l2, key=lambda x: x.get(key)))
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
    def _combine_partial_responses(partial_responses: List[List[Dict]], required_field: str):
        if not partial_responses:
            return partial_responses
        if not isinstance(partial_responses[0], list):
            return partial_responses

        response = partial_responses[0]
        partial_responses_count = len(partial_responses)

        for index in range(1, partial_responses_count):
            response = [{**u, **v} for u, v in
                        GraphAPIGetHelper.sorted_zip_longest(response, partial_responses[index],
                                                             key=required_field, fillvalue={})]
        return response


    @staticmethod
    def _get_fields_partitions(fields: list, required_field: str = None):
        n = len(fields)
        indices = range(0, n, GraphAPIGetHelper.__fields_num)
        for index in indices:
            if required_field:
                yield list(set(fields[index : index + GraphAPIGetHelper.__fields_num] + [required_field]))
            else:
                yield list(set(fields[index : index + GraphAPIGetHelper.__fields_num]))
