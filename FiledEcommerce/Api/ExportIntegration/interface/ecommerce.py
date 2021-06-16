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

    @classmethod
    @abstractmethod
    def pre_install(cls, request):
        pass

    @classmethod
    @abstractmethod
    def app_install(cls, request):
        pass

    @classmethod
    @abstractmethod
    def app_load(cls, request):
        pass

    @classmethod
    @abstractmethod
    def app_uninstall(cls, request):
        pass
