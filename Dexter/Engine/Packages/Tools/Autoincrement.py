class Autoincrement:

    def __init__(self, value):
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

    def increment(self):
        self.__id += 1
        return self.__id

    def increment_as_string(self):
        self.__id += 1
        return self.__id_to_string(self.__id)

    @staticmethod
    def __id_to_string(x):
        return "__" + str(x)