# This file is placed in the Public Domain.

"client"


from .hdl import Handler, dispatch


def __dir__():
    return (
            'Client',
           )


class Client(Handler):

    """
        client handler, add input/output.
    """

    def __init__(self):
        Handler.__init__(self)
        self.ignore = []
        self.orig = repr(self)
        self.register("event", dispatch)

    def announce(self, txt: str) -> None:
        "annouce text."
        self.raw(txt)

    def raw(self, txt: str) -> None:
        "raw echo of text."
        raise NotImplementedError("raw")

    def say(self, channel: str, txt: str) -> None:
        "say text into channel."
        if channel not in self.ignore:
            self.raw(txt)
