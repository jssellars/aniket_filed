import os


class LoadObjects:
    objects = []

    __python_init_file_name = "__init__.py"
    __python_extension = ".py"

    @classmethod
    def load_objects(cls, path=None, onlyLocal=False):
        if path is None:
            modules = os.listdir(os.path.dirname(__file__))
        else:
            modules = os.listdir(path)

        for module in modules:
            module_name, module_extension = os.path.splitext(module)
            if module == cls.__python_init_file_name or module_extension != cls.__python_extension:
                continue
            if onlyLocal:
                __import__(module_name, locals())
            else:
                __import__(module_name, locals(), globals())
