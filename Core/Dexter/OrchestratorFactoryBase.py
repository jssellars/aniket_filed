from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum


class OrchestratorFactoryBase:
    _factory = {
        # implement this if you want to extend this class
    }

    @classmethod
    def get(cls, strategy):
        if not cls._factory:
            raise NotImplementedError
        orchestrator = cls._factory.get((strategy,), None)
        return orchestrator
