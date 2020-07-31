from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum


class RuleEvaluatorFactoryBase:
    _factory = {
        # if you extend this, implement the _factory
    }

    @classmethod
    def get(cls, algorithm_type, level: LevelEnum = None):
        if not cls._factory:
            raise NotImplementedError
        rule_evaluator = cls._factory.get((algorithm_type, level), None)
        return rule_evaluator
