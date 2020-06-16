import typing

from GoogleDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import Fuzzyfier


class FuzzyfierCollectionBase:
    _collection = []

    def add_fuzzyfier(self, fuzzifier: Fuzzyfier = None):
        self._collection.append(fuzzifier)
        return self

    def get_by_metric_name(self, metric_name: typing.AnyStr = None):
        return next(filter(lambda x: x.metric_name == metric_name, self._collection), None)
