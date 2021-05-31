from abc import ABC, abstractmethod


class Ecommerce(ABC):
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
