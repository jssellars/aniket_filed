from Core.Dexter.OrchestratorFactoryBase import OrchestratorFactoryBase
from FacebookDexter.Engine.MasterWorker.DefaultFacebookOrchestrator import DefaultFacebookOrchestrator
from FacebookDexter.Engine.MasterWorker.FacebookStrategyEnum import FacebookStrategyEnum
from FacebookDexter.Engine.MasterWorker.SingleMetricOrchestrator import SingleMetricOrchestrator


class FacebookOrchestratorFactory(OrchestratorFactoryBase):
    _factory = {
        (FacebookStrategyEnum.DEFAULT,): DefaultFacebookOrchestrator(),
        (FacebookStrategyEnum.SINGLE_METRIC,): SingleMetricOrchestrator()
    }
