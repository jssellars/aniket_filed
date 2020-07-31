import typing

from Core.Dexter.Engine.Algorithms.AlgorithmsEnumBase import AlgorithmsEnumBase
from Core.Dexter.Engine.Algorithms.FuzzyRuleBasedOptimization.StrategyBaseEnum import StrategyBaseEnum
from Core.Dexter.Engine.Algorithms.NoActionAlgorithm import NoActionAlgorithm
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationAdLevel import \
    FacebookRuleBasedOptimizationAdLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationAdSetLevel import \
    FacebookRuleBasedOptimizationAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationCampaignLevel import \
    FacebookRuleBasedOptimizationCampaignLevel

AlgorithmType = typing.Union[FacebookRuleBasedOptimizationCampaignLevel,
                             FacebookRuleBasedOptimizationAdSetLevel,
                             FacebookRuleBasedOptimizationAdLevel,
                             typing.NoReturn]


class AlgorithmsFactoryBase:
    _factory = {
        # implement this if you want to extend the class
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnumBase = None, level: LevelEnum = None,
            channel: ChannelEnum = None, strategy: StrategyBaseEnum = None) -> AlgorithmType:
        if not cls._factory:
            raise NotImplementedError
        algorithm = cls._factory.get((algorithm_type, level, channel, strategy), NoActionAlgorithm())
        return algorithm
