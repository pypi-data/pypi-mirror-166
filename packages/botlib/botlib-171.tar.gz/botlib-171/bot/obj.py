# This file is placed in the Public Domain.
# pylint: disable=W0613


"big Object"


import datetime
import os
import types
import uuid


def __dir__():
    return (
            'Object',
            'edit',
            'find',
            'get',
            'items',
            'iter',
            'keys',
            'otype',
            'getname',
            'printable',
            'register',
            'search',
            'update',
            'values'
           )


class Object:

    "big Object"

    __slots__ = (
        '__dict__',
        '__stp__'
    )



    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.__stp__ = os.path.join(
            otype(self),
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            update(self, args[0])

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self. __dict__)


def delete(obj: Object, key: str) -> None:
    "delete key from object."
    delattr(obj, key)


def edit(obj: Object, setter: dict) -> None:
    "edit object using a setter."
    for key, value in items(setter):
        register(obj, key, value)


def get(obj: Object, key: str, default: str = None) -> object:
    "return value by key."
    return obj.__dict__.get(key, default)


def getname(obj: Object) -> str:
    "return full qualified name of a object."
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def items(obj: Object) -> list[object]:
    "return items (key/value)."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj: Object) -> list[str]:
    "return keys."
    return obj.__dict__.keys()


def otype(obj: Object) -> str:
    "return type of a object."
    return str(type(obj)).split()[-1][1:-2]


def printable(
              obj: Object,
              args: str = "",
              skip: str = "",
              plain: bool = False
             ) -> str:
    "return printable string of an object."
    res = []
    try:
        keyz = args.split(",")
    except (AttributeError, TypeError, ValueError):
        keyz = keys(obj)
    for key in keyz:
        try:
            skips = skip.split(",")
            if key in skips or key.startswith("_"):
                continue
        except (TypeError, ValueError):
            pass
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    return " ".join(res)


def register(obj: Object, key: str, value: object) -> None:
    "set a key/value."
    setattr(obj, key, value)


def update(obj: Object, data: Object) -> None:
    "slurp in some data."
    if isinstance(data, type({})):
        obj.__dict__.update(data)
    else:
        obj.__dict__.update(vars(data))


def values(obj: Object) -> list[object]:
    "return values."
    return obj.__dict__.values()
