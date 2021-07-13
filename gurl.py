from types import CodeType, FunctionType
from functools import wraps

class URLComponent(object):
    def __init__(self, first_part='/'):
        self.parts = [first_part]

    def request(self, *args, **kwargs):
        import requests
        url = str(self)
        return requests.request(url=url, *args, **kwargs)

    def __str__(self):
        return "http://" + '/'.join(self.parts)

    def __truediv__(self, path):
        if type(path) == str:
            self.parts.append(path)
        elif type(path) == URLComponent:
            self.parts.append('/'.join(path.parts))
        return self

    def __getattribute__(self, name):
        if name not in ['parts', 'request']:
            self.parts[-1] += f".{name}"
            return self
        return object.__getattribute__(self, name)


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
                                    old_func.__name__, old_func.__defaults__)
        return new_function()

    return wrapper
