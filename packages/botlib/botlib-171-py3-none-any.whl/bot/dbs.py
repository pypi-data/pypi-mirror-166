# This file is placed in the Public Domain.
# pylint: disable=R0903,W0212


"database"


import os
import _thread


from .dft import Default
from .jsn import load
from .obj import Object, get, items, otype, update
from .tbl import Class
from .utl import locked, fntime
from .wdr import getpath


def __dir__():
    return (
            'Dbs',
            'fns',
            'hook',
            'search',
            'find',
            'last'
           )


dblock = _thread.allocate_lock()


class Selector(Default):

    "selector class."


class Dbs():

    "database functions."

    @staticmethod
    def all(otp, timed: dict = None) -> list[Object]:
        "return all object of a type."
        result = []
        for fnm in fns(getpath(otp), timed):
            obj = hook(fnm)
            if "__deleted__" in obj and obj.__deleted__:
                continue
            if "_deleted" in obj and obj._deleted:
                continue
            result.append((fnm, obj))
        if not result:
            return []
        return result

    @staticmethod
    def find(otp, selector: dict = None, index: int = None, timed: dict = None)  -> list[Object]:
        "find specific objects."
        if selector is None:
            selector = {}
        _nr = -1
        result = []
        for fnm in fns(getpath(otp), timed):
            obj = hook(fnm)
            if selector and not search(obj, selector):
                continue
            if "__deleted__" in obj and obj.__deleted__:
                continue
            if "_deleted" in obj and obj._deleted:
                continue
            _nr += 1
            if index is not None and _nr != index:
                continue
            result.append((fnm, obj))
        return result

    @staticmethod
    def last(otp: str) -> tuple[str, Object]:
        "return the last object of a type."
        fnm = fns(getpath(otp))
        if fnm:
            fnn = fnm[-1]
            return (fnn, hook(fnn))
        return (None, None)

    @staticmethod
    def match(otp, selector: dict = None, index: int = None, timed: dict = None) -> [str, Object]:
        "return last matching object."
        res = sorted(
                     find(otp, selector, index, timed),
                     key=lambda x: fntime(x[0])
                    )
        if res:
            return res[-1]
        return (None, None)


@locked(dblock)
def fns(path: str, timed: dict = None) -> list[str]:
    "return all filenames."
    if not path:
        return []
    if not os.path.exists(path):
        return []
    res = []
    dpath = ""
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        if dirs:
            dpath = sorted(dirs)[-1]
            if dpath.count("-") == 2:
                ddd = os.path.join(rootdir, dpath)
                fls = sorted(os.listdir(ddd))
                if fls:
                    opath = os.path.join(ddd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(opath) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(opath) > timed.to:
                        continue
                    res.append(opath)
    return sorted(res, key=fntime)


@locked(dblock)
def hook(hfn: str) -> Object:
    "reconstruct from filename."
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    cls = Class.get(cname)
    if cls:
        obj = cls()
    else:
        obj = Object()
    fnm = os.sep.join(oname)
    load(obj, fnm)
    return obj


def search(obj: Object, selector: dict) -> bool:
    "check if object is matching the selector."
    res = False
    select = Selector(selector)
    for key, value in items(select):
        val = get(obj, key)
        if value in str(val):
            res = True
            break
    return res


def find(name: str, selector: dict = None, index: dict = None, timed: dict = None) -> list[Object]:
    "find an object by small name."
    names = Class.full(name)
    dbs = Dbs()
    for nme in names:
        for fnm, obj in dbs.find(nme, selector, index, timed):
            yield fnm, obj


def last(obj: Object) -> None:
    "populate an object with the last version."
    dbs = Dbs()
    _path, _obj = dbs.last(otype(obj))
    if _obj:
        update(obj, _obj)
