import typing
from datetime import timedelta
from queue import Queue
from threading import Thread

from dateutil.parser import parse

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationBase import \
    FacebookRuleBasedOptimizationBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookAvailableMetricEnum import \
    FacebookAvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookActionBreakdownEnum, FacebookBreakdownEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricCalculator import FacebookMetricCalculator


import logging

logger = logging.getLogger(__name__)


class FacebookRuleBasedOptimizationCampaignLevel(FacebookRuleBasedOptimizationBase):

    def __init__(self):
        super().__init__()
        self.set_level(LevelEnum.CAMPAIGN)

    def run(self, campaign_id: typing.AnyStr = None, rule_selection_types: typing.List = None) -> typing.List[
        typing.Dict]:
        recommendations = []
        if self.is_available(campaign_id):
            que = Queue()
            threads_list = []
            for rule_selection_type in rule_selection_types:
                for evaluate_function in self.rules_selector(rule_selection_type):
                    thread = Thread(target=lambda q, arg1, arg2: q.put(evaluate_function(arg1, arg2)),
                                    args=(que, campaign_id, self._fuzzyfier_factory))
                    threads_list.append(thread)

            for thread in threads_list:
                thread.start()

            for thread in threads_list:
                thread.join()

            while not que.empty():
                recommendations += que.get()

        return recommendations

    def check_run_status(self, campaign_id):
        if self.__check_last_x_days_since_update(campaign_id):
            return True

        result = self.__check_in_last_x_days(campaign_id)
        return result

    def __check_in_last_x_days(self, campaign_id):
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=self._dexter_config.days_since_last_change)
        breakdown_metadata = BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                               action_breakdown=FacebookActionBreakdownEnum.NONE)
        time_interval = (date_stop - date_start).days
        results, _ = (FacebookMetricCalculator().
                      set_metric(FacebookAvailableMetricEnum.RESULTS.value).
                      set_breakdown_metadata(breakdown_metadata).
                      set_facebook_id(campaign_id).
                      set_repository(self._mongo_repository).
                      set_level(self._level).
                      set_date_stop(self._date_stop).
                      compute_value(atype=AntecedentTypeEnum.VALUE, time_interval=time_interval))

        if results >= self._dexter_config.min_results:
            return True
        else:
            logger.debug(
                f"Campaign {campaign_id} has less than {self._dexter_config.min_results} results",
                extra={"values": results, "facebook_id": campaign_id, "config": self._dexter_config},
            )
            return False

    def __check_last_x_days_since_update(self, campaign_id):
        structure_details = self._mongo_repository.get_structure_details(key_value=campaign_id,
                                                                         level=LevelEnum.CAMPAIGN)
        try:
            updated_time = parse(structure_details.get('updated_time')).date()
        except:
            try:
                updated_time = parse(structure_details.get('created_time')).date()
            except Exception as e:
                logger.debug(
                    f"Campaign {campaign_id} does not have updated time nor created time || {repr(e)}",
                    extra={"facebook_id": campaign_id, "config": self._dexter_config},
                )
                return False
        date_stop = self._date_stop.date()

        if (date_stop - updated_time).days >= self._dexter_config.recommendation_days_last_updated:
            breakdown_metadata = BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                   action_breakdown=FacebookActionBreakdownEnum.NONE)
            time_interval_days = (date_stop - updated_time).days
            fbmc = (FacebookMetricCalculator().
                    set_metric(FacebookAvailableMetricEnum.RESULTS.value).
                    set_breakdown_metadata(breakdown_metadata).
                    set_facebook_id(campaign_id).
                    set_repository(self._mongo_repository).
                    set_level(self._level).
                    set_date_stop(self._date_stop))
            results, _ = (fbmc.compute_value(atype=AntecedentTypeEnum.VALUE, time_interval=time_interval_days))

            if results >= self._dexter_config.min_results:
                return True
            else:
                logger.debug(
                    f"Campaign {campaign_id} has less than {self._dexter_config.min_results} results",
                    extra={"values": results, "facebook_id": campaign_id, "config": self._dexter_config}
                )
        else:
            logger.debug(
                f"A more recent change was not made for {campaign_id}"
                f" in the last {self._dexter_config.days_since_last_change} days",
                extra={"facebook_id": campaign_id, "config": self._dexter_config}
            )

        return False
