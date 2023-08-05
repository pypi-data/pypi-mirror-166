# This file is placed in the Public Domain.


"table"


from typing import Callable


from .obj import Object, delete, get, register


def __dir__():
    return (
            'Bus',
            'Callbacks',
            'Class',
            'Commands',
            'Table'
           )


class Bus():

    "list of bots"

    objs = []

    @staticmethod
    def add(obj: Object) -> None:
        "add a listener to the bus."
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt: str) -> None:
        "annouce text on the joined listeners."
        for obj in Bus.objs:
            if obj and "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def byorig(orig: str) -> Object:
        "return listener by origin (repr)."
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig: str, channel: str, txt: str) -> None:
        "say text into channel of specific listener."
        obj = Bus.byorig(orig)
        if obj and "say" in dir(obj):
            obj.say(channel, txt)


class Callbacks():

    "callbacks"

    cbs = Object()

    @staticmethod
    def add(typ: str, cbs: Callable[Object, None]) -> None:
        "add a callback."
        if typ not in Callbacks.cbs:
            register(Callbacks.cbs, typ, cbs)

    @staticmethod
    def callback(event: Object) -> None:
        "run a callback (on event.type)."
        func = Callbacks.get(event.type)
        if not func:
            event.ready()
            return
        func(event)

    @staticmethod
    def dispatch(event: Object) -> None:
        "dispatch an event."
        Callbacks.callback(event)

    @staticmethod
    def get(typ: str) -> Callable[Object, None]:
        "return callback."
        return get(Callbacks.cbs, typ)


class Class():

    "registered classes that can be saved."

    cls = {}

    @staticmethod
    def add(clz: type[object]) -> None:
        "add a class."
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def full(name: str) -> list[str]:
        "return matching class names."
        name = name.lower()
        res = []
        for cln in Class.cls:
            if cln.split(".")[-1].lower() == name:
                res.append(cln)
        return res

    @staticmethod
    def get(name: str) -> type[object]:
        "return specific class name."
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name: str) -> None:
        "remove a class name."
        del Class.cls[name]


Class.add(Object)


class Commands():

    "commands."

    cmds = Object()

    @staticmethod
    def add(cmd: Callable[Object, None]) -> None:
        "add a command."
        register(Commands.cmds, cmd.__name__, cmd)

    @staticmethod
    def get(cmd: str) -> Callable[Object, None]:
        "return a command."
        return get(Commands.cmds, cmd)

    @staticmethod
    def remove(cmd: str) -> None:
        "remove a command."
        delete(Commands.cmds, cmd)


class Table():

    "table"

    mods = Object()

    @staticmethod
    def add(mod: type[object]) -> None:
        "add a module."
        register(Table.mods, mod.__name__, mod)

    @staticmethod
    def get(modname: str) -> type[object]:
        "return a module."
        return get(Table, modname)

    @staticmethod
    def remove(modname: str) -> None:
        "remove a module."
        delete(Table.mods, modname)
