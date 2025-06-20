import json
import importlib
import inspect
import types
import builtins
import random
from abc import ABC, abstractmethod


def _make_cell(val):
    def inner():
        return val
    return inner.__closure__[0]


def _serialize_value(val):
    if isinstance(val, StringCounter):
        return val._to_data()
    if isinstance(val, (list, tuple)):
        return [_serialize_value(v) for v in val]
    if isinstance(val, dict):
        return {k: _serialize_value(v) for k, v in val.items()}
    if isinstance(val, random.Random):
        return {"__random_state__": val.getstate()}
    if isinstance(val, types.BuiltinFunctionType):
        return {"__builtin_func__": True, "name": val.__name__}
    if callable(val):
        try:
            raw_lines, start = inspect.getsourcelines(val)
            idx = val.__code__.co_firstlineno - start
            line = raw_lines[idx].strip()
            if 'lambda ' in line:
                src = line[line.index('lambda'):].rstrip(',')
                while src.endswith(']') and src.count('[') < src.count(']'):
                    src = src[:-1]
                source = src
            else:
                source = line
        except (OSError, IOError, IndexError):
            raw = inspect.getsource(val)
            source = raw.strip()
        defaults = val.__defaults__
        serialized_defaults = _serialize_value(defaults) if defaults else None
        closure = val.__closure__
        if closure:
            cl_values = [c.cell_contents for c in closure]
            serialized_values = _serialize_value(cl_values)
            closure_names = val.__code__.co_freevars
            closure_data = {
                "names": closure_names,  # just for readability
                "values": serialized_values,
            }
        else:
            closure_data = None
        return {
            "__func__": True,
            "source": source,
            "defaults": serialized_defaults,
            "closure": closure_data,
            "globals": val.__code__.co_names,
            "name": val.__name__,
        }
    if isinstance(val, (str, int, float, bool)) or val is None:
        return val
    raise TypeError(f"Cannot serialize type {type(val)}")


def _deserialize_value(data):
    if isinstance(data, dict):
        if "__class__" in data and "__module__" in data and "__attrs__" in data:
            module = importlib.import_module(data["__module__"])
            cls = getattr(module, data["__class__"])
            obj = object.__new__(cls)
            attrs = data["__attrs__"]
            for k, v in attrs.items():
                setattr(obj, k, _deserialize_value(v))
            return obj
        if "__random_state__" in data:
            def _to_tuple(x):
                if isinstance(x, list):
                    return tuple(_to_tuple(v) for v in x)
                return x

            state = _to_tuple(data["__random_state__"])
            rng = random.Random()
            rng.setstate(state)
            return rng
        if data.get("__func__"):
            source = data.get("source", "").strip()
            globs = {name: builtins.__dict__[name] for name in data.get("globals", []) if name in builtins.__dict__}
            globs["__builtins__"] = builtins
            if source.startswith("lambda"):
                func = eval(source, globs)
            elif source.startswith("def"):
                loc = {}
                exec(source, globs, loc)
                func = loc[data["name"]]
            else:
                func = eval(source, globs)
            if data.get("defaults") is not None:
                func.__defaults__ = tuple(_deserialize_value(data["defaults"]))
            if data.get("closure"):
                vals = _deserialize_value(data["closure"]["values"])
                cells = tuple(_make_cell(v) for v in vals)
                func = types.FunctionType(func.__code__, func.__globals__, func.__name__, func.__defaults__, cells)
            return func
        if data.get("__builtin_func__"):
            return getattr(builtins, data["name"])
        return {k: _deserialize_value(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_deserialize_value(v) for v in data]
    return data


class StringCounter(ABC):
    @abstractmethod
    def count(self, s: str) -> int:
        """
        Count the given string and return an integer.

        :param s: The input string to be counted
        :return: An integer result of the counting process
        """
        pass

    def __call__(self, s: str) -> int:
        """
        Make the object callable, equivalent to calling the count method.

        :param s: The input string to be counted
        :return: An integer result of the counting process
        """
        return self.count(s)

    def _to_data(self):
        return {
            "__class__": self.__class__.__name__,
            "__module__": self.__class__.__module__,
            "__attrs__": _serialize_value(self.__dict__),
        }

    def serialize(self):
        """
        Serialize the counter object to a JSON string.

        :return: Serialized version of the counter object
        """
        return json.dumps(self._to_data())

    @classmethod
    def deserialize(cls, data) -> "StringCounter":  # type: ignore
        """
        Deserialize data into a StringCounter object.

        :param data: Serialized JSON string of a StringCounter object
        :return: Deserialized StringCounter object
        """
        if isinstance(data, (bytes, bytearray)):
            data = data.decode()
        return _deserialize_value(json.loads(data))
