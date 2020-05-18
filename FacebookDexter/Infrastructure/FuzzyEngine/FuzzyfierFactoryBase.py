import typing
from collections import defaultdict
from operator import setitem

from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzyfierCollectionBase import FuzzyfierCollectionBase


class FuzzyfierFactoryBase:

    def __init__(self, fuzzyfier_collection: typing.Dict = None):
        if fuzzyfier_collection:
            self._fuzzyfiers = fuzzyfier_collection
        else:
            self._fuzzyfiers = defaultdict(None)

    def get_fuzzyfier(self, fuzzyfier_type: AntecedentTypeEnum = None, metric_name: typing.AnyStr = None):
        fuzzyfiers = self._fuzzyfiers.get(fuzzyfier_type)
        if not fuzzyfiers:
            raise UserWarning(f"Could not find fuzzyfier collection {fuzzyfier_type.value}.")
        return next(filter(lambda x: x.metric_name == metric_name, fuzzyfiers), None)

    def add_fuzzyfiers(self, fuzzyfier_type: AntecedentTypeEnum = None, fuzzyfier: FuzzyfierCollectionBase = None):
        setitem(self._fuzzyfiers, fuzzyfier_type, fuzzyfier)
        return self
