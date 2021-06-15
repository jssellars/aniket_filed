from abc import ABC, abstractmethod


class Ecommerce(ABC):
 
    @classmethod
    @abstractmethod
    def mapper(cls):
        pass

    @classmethod
    @abstractmethod
    def export(cls, request):
        pass