import hashlib
import random
import typing


class Autoincrement:

    def __init__(self, value: int = None):
        self.__id = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @id.deleter
    def id(self):
        delattr(self, "__id")

    def increment(self) -> int:
        self.__id += 1
        return self.__id

    def increment_as_string(self) -> typing.AnyStr:
        self.__id += 1
        return self.__id_to_string(self.__id)

    @staticmethod
    def __id_to_string(x: int = None) -> typing.AnyStr:
        return "__" + str(x)

    @staticmethod
    def hex_string(value: typing.AnyStr = None) -> typing.AnyStr:
        if value is None:
            value = str(random.randint(0, 1e20))
        hex_string_value = hashlib.sha1(value.encode('utf-8')).hexdigest()
        return hex_string_value
