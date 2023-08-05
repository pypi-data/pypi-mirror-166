# This file is placed in the Public Domain.


"thread"


import queue
import threading


from typing import Callable


from .obj import getname


def __dir__():
    return (
            'Thread',
            'launch'
           )


class Thread(threading.Thread):

    "implements a iterable, result returning on join, thread."

    def __init__(self, func, name, *args, daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._exc = None
        self._evt = None
        self.name = name or getname(func)
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self.sleep = None
        self.state = None
        self._result = None

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout: int = None) -> list[type[object]]:
        "join this thread."
        super().join(timeout)
        return self._result

    def run(self) -> None:
        "run the thead's function."
        func, args = self.queue.get()
        if args:
            self._evt = args[0]
        self.setName(self.name)
        self._result = func(*args)


def launch(func: Callable[object, None], *args, **kwargs) -> Thread:
    "run a function into a thread."
    nme = kwargs.get("name", getname(func))
    thr = Thread(func, nme, *args)
    thr.start()
    return thr
