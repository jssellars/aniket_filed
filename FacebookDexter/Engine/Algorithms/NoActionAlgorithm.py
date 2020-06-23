import typing

from FacebookDexter.Engine.Algorithms.NoActionAlgorithmBuilder import NoActionAlgorithmBuilder


class NoActionAlgorithm(NoActionAlgorithmBuilder):

    def __init__(self):
        super().__init__()

    def run(self, structure_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        return []

    def check_run_status(self, campaign_id: typing.AnyStr = None):
        return True