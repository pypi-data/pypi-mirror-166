# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,C0413,C0411,R0903


"log"


import time


from .dbs import find
from .obj import Object
from .jsn import save
from .utl import elapsed, fntime


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def log(event):
    if not event.rest:
        _nr = 0
        for _fn, obj in find("log"):
            event.reply("%s %s %s" % (
                                      _nr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(_fn)))
                                     )
            _nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    save(obj)
    event.reply("ok")
