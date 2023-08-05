# This file is placed in the Public Domain.
# pylint: disable=R0903


"default"


from .obj import Object


def __dir__():
    return (
            'Default',
           )


class Default(Object):

    "provides returning a default value."

    __slots__ = ("__default__",)

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__default__ = ""

    def __getattr__(self, key: str):
        return self.__dict__.get(key, self.__default__)
