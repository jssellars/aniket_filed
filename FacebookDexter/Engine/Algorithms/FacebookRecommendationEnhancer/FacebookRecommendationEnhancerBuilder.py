import typing
from datetime import datetime

from Core.Tools.Logger.MongoLoggers.MongoLogger import MongoLogger
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.RuleBasedOptimizationFuzzyfierFactory import \
    RuleBasedOptimizationFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBuilder import \
    RuleBasedOptimizationBuilder
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.Rules import Rules
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluator import RuleEvaluator
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class FacebookRecommendationEnhancerBuilder(RuleBasedOptimizationBuilder):
    def __init__(self):
        super().__init__()