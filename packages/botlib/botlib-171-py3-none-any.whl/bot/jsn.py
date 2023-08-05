# This file is placed in the Public Domain.
# pylint: disable=W0221

"json"


import datetime
import json
import os


from json import JSONDecoder, JSONEncoder


from .obj import Object, update
from .utl import cdir
from .wdr import Wd, getpath


def __dir__():
    return (
            'ObjectDecoder',
            'ObjectEncoder',
            'dump',
            'dumps',
            'load',
            'loads',
            'save'
           )


class ObjectDecoder(JSONDecoder):

    "decode string to object."

    def  __init__(self, *args, **kwargs):
        ""
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, inp: str, _w=None) -> Object:
        "do the decoding."
        value = json.loads(inp)
        return Object(value)

    def raw_decode(self, inp: str, *args, **kwargs) -> Object:
        "deconding of raw string."
        return JSONDecoder.raw_decode(self, inp, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    "encode to object from string."

    def  __init__(self, *args, **kwargs):
        ""
        JSONEncoder.__init__(self, *args, **kwargs)

    def encode(self, obj: Object) -> str:
        "encode object to string."
        return JSONEncoder.encode(self, obj)

    def default(self, obj: Object) -> str:
        "return default string for object."
        if isinstance(obj, dict):
            return obj.items()
        if isinstance(obj, Object):
            return vars(obj)
        if isinstance(obj, list):
            return iter(obj)
        if isinstance(obj,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return obj
        try:
            return JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

    def iterencode(self, obj: Object, *args, **kwargs):
        "iterate while encoding."
        return JSONEncoder.iterencode(self, obj, *args, **kwargs)


def dump(obj: Object, opath: str) -> str:
    "dump object to file."
    cdir(opath)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            obj.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return obj.__stp__


def dumps(obj: Object) -> str:
    "return json string."
    return json.dumps(obj, cls=ObjectEncoder)


def load(obj: Object, opath: str) -> None:
    "load object from path."
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)
    obj.__stp__ = stp


def loads(jss: str) -> Object:
    "return object from json string."
    return json.loads(jss, cls=ObjectDecoder)


def save(obj: Object) -> str:
    "save an object to disk."
    prv = os.sep.join(obj.__stp__.split(os.sep)[:2])
    obj.__stp__ = os.path.join(
                       prv,
                       os.sep.join(str(datetime.datetime.now()).split())
                      )
    opath = getpath(obj.__stp__)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return obj.__stp__
