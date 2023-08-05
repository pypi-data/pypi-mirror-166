# This file is placed in the Public Domain.
# pylint: disable=W0613


"utility"


import os
import pathlib
import time
import _thread


dblock = _thread.allocate_lock()


def __dir__():
    return (
            'cdir',
            'locked',
            'elapsed',
            'fntime',
            'getlist',
            'gettypes',
            'listfiles',
            'spl'
           )


def locked(lock):

    "locking decorator (provide the lock)."

    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        return lockedfunc

    return lockeddec


def cdir(path: str) -> None:
    "create directory."
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def elapsed(seconds: int, short: bool = True) -> str:
    "elapsed number of seconds to a string."
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def fntime(daystr: str) -> float:
    "create time from a file path."
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.split(".")[0]
    return time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))


def getlist() -> list[str]:
    "return comma seperated list in a file named CFG."
    return [x.strip() for x in open("CFG", "r").readlines()[-1].split(",")]


def gettypes(path: str) -> list[str]:
    "return types in store."
    path = os.path.join(path, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def listfiles(workdir: str) -> list[str]:
    "list files in store."
    path = os.path.join(workdir, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def spl(txt: str) -> list:
    "split comma seperated string into list."
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
