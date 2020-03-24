from enum import Enum
from Config import Endpoints


class OptimizeTables(Enum):
    Endpoint = Endpoints.get_optimization_endpoint()
    Goals = "FiledOptimizations"


class Columns(Enum):
    Id = "FacebookId"
    Goal = "Goal"