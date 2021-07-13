from types import CodeType, FunctionType
from functools import wraps


class URLComponent(object):
    def __init__(self, first_part='/'):
        self.__parts = [first_part]

    def __call__(self, *args, **kwargs):
        import requests
        url = str(self)
        kwargs.setdefault('method', 'GET')
        return requests.request(url=str(self), *args, **kwargs)

    def __str__(self):
        return "http://" + '/'.join(self.__parts)

    def __truediv__(self, path):
        if type(path) == str:
            self.__parts.append(path)
        elif type(path) == URLComponent:
            self.__parts.append('/'.join(path.__parts))
        return self

    def __getattribute__(self, name):
        try:
            if object.__getattribute__(self, name):
                return object.__getattribute__(self, name)
        except AttributeError:
            self.__parts[-1] += f".{name}"
            return self


def genius_url(old_func: FunctionType):
    class FakeGlobals(dict):
        def __init__(self, d):
            self.update(d)

        def __getitem__(self, key):
            if key not in self:
                if key in self['__builtins__'].__dict__:
                    return self['__builtins__'].__dict__[key]
                return URLComponent(key)
            return dict.__getitem__(self, key)

    @wraps(old_func)
    def wrapper(*args, **kwds):
        new_function = FunctionType(old_func.__code__,
                                    FakeGlobals(old_func.__globals__),
                                    old_func.__name__, old_func.__defaults__, old_func.__closure__)
        return new_function()

    return wrapper
