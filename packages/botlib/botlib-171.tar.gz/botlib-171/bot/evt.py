# This file is placed in the Public Domain.


"event"


import threading


from .dft import Default
from .obj import Object, update
from .prs import parse
from .tbl import Bus


def __dir__():
    return (
            'Event',
           )


class Event(Default):

    "basic event."

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._result = []
        self.orig = repr(self)
        self.type = "event"

    def bot(self) -> Object:
        "return originating bot."
        return Bus.byorig(self.orig)

    def parse(self) -> None:
        "parse the event."
        if self.txt:
            update(self, parse(self.txt))

    def ready(self) -> None:
        "signal event as ready."
        self._ready.set()

    def reply(self, txt: str) -> None:
        "add text to the result."
        self._result.append(txt)

    def show(self) -> None:
        "display results."
        for txt in self._result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self) -> list:
        "wait for event to be ready."
        self._ready.wait()
        return self._result
