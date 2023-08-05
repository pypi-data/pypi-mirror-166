# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,C0413,C0411,R0903


"todo"


import time


from .dbs import find
from .jsn import save
from .obj import Object
from .utl import elapsed, fntime


class Todo(Object):

    "a todo item."

    def __init__(self):
        super().__init__()
        self.txt = ""


def dne(event):
    "flag a todo done."
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for _fn, obj in find("todo", selector):
        obj.__deleted__ = True
        save(obj)
        event.reply("ok")
        break


def tdo(event):
    "add a todo."
    if not event.rest:
        _nr = 0
        for _fn, obj in find("todo"):
            event.reply("%s %s %s" % (_nr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(_fn))))
            _nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    save(obj)
    event.reply("ok")
