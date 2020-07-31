from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum


class RulesFactoryBase:
    _factory = {
        # if you extend this, implement the _factory
    }

    @classmethod
    def get(cls, algorithm_type, level: LevelEnum = None):
        if not cls._factory:
            raise NotImplementedError
        rules = cls._factory.get((algorithm_type, level), None)
        return rules
