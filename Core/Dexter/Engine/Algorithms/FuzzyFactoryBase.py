from Core.Dexter.Engine.Algorithms.AlgorithmsEnumBase import AlgorithmsEnumBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum


class FuzzyFactoryBase:
    _factory = {
        # if you extend this, implement the _factory
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnumBase = None, level: LevelEnum = None):
        if not cls._factory:
            raise NotImplementedError
        fuzzyfier_factory = cls._factory.get((algorithm_type, level), None)
        return fuzzyfier_factory
