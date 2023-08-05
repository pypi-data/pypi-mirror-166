# This file is placed in the Public Domain.


"handler"


import queue
import threading
import time


from collections.abc import Callable


from .evt import Event
from .obj import Object
from .tbl import Bus, Callbacks, Commands
from .thr import launch


def __dir__():
    return (
            'Handler',
            'dispatch'
           )


class Handler(Object):

    "event handler."

    def __init__(self):
        Object.__init__(self)
        self.cache = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Bus.add(self)

    @staticmethod
    def forever() -> None:
        "run forever."
        while 1:
            time.sleep(1.0)

    @staticmethod
    def handle(event: Event) -> None:
        "handle the event."
        Callbacks.dispatch(event)

    def loop(self) -> None:
        "handle events until stopped."
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self) -> Event:
        "return an event to be handled."
        return self.queue.get()

    def put(self, event: Event) -> None:
        "put an event into the waiting queue."
        self.queue.put_nowait(event)

    @staticmethod
    def register(typ: str, cbs: Callable[Event, None]) -> None:
        "register a callback."
        Callbacks.add(typ, cbs)

    def restart(self) -> None:
        "stop/start the handler."
        self.stop()
        self.start()

    def start(self) -> None:
        "start the handler."
        self.stopped.clear()
        launch(self.loop)

    def stop(self) -> None:
        "stop the handler."
        self.stopped.set()


def dispatch(evt: Event):
    "dispatch an event."
    evt.parse()
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()
