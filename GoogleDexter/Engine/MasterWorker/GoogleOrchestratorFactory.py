from Core.Dexter.OrchestratorFactoryBase import OrchestratorFactoryBase
from GoogleDexter.Engine.MasterWorker.DefaultGoogleOrchestrator import DefaultGoogleOrchestrator
from GoogleDexter.Engine.MasterWorker.GoogleStrategyEnum import GoogleStrategyEnum


class GoogleOrchestratorFactory(OrchestratorFactoryBase):
    _factory = {
        (GoogleStrategyEnum.DEFAULT,): DefaultGoogleOrchestrator()
    }
