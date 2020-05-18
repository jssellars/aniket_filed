import os


class LoadObjects:
    objects = []

    __python_init_filename = "__init__.py"
    __python_extension = ".py"

    @classmethod
    def load(cls, path=None, only_local=False):
        if path is None:
            modules = os.listdir(os.path.dirname(__file__))
        else:
            modules = os.listdir(path)

        for module in modules:
            module_name, module_extension = os.path.splitext(module)
            if module == cls.__python_init_filename or module_extension != cls.__python_extension:
                continue
            if only_local:
                __import__(module_name, locals())
            else:
                __import__(module_name, locals(), globals())
