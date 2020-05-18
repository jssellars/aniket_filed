import inspect
import json


class ObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, "to_json"):
            try:
                return self.default(obj.to_json())
            except TypeError as type_error:
                return
            except Exception as e:
                raise e
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not key.startswith("_")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
                and not (isinstance(value, list) and not value)
                and not (isinstance(value, dict) and not value)
            )
            return self.default(d)
        return obj
