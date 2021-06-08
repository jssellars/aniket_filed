from abc import ABC, abstractmethod


class Ecommerce(ABC):
    @classmethod
    @abstractmethod
    def mapper(cls, data, mapping):
        pass

    @classmethod
    @abstractmethod
    def get_products(cls, data):
        pass

    @classmethod
    @abstractmethod
    def pre_install(cls):
        pass

    @classmethod
    @abstractmethod
    def app_install(cls):
        pass

    @classmethod
    @abstractmethod
    def app_load(cls):
        pass

    @classmethod
    @abstractmethod
    def app_uninstall(cls):
        pass
