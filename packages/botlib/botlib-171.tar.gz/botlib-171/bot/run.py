# This file is placed in the Public Domain.


"runtime"


import time


from .clt import Client
from .dft import Default
from .evt import Event


def __dir__():
    return (
            'Cfg',
            'docmd',
            'starttime',
            'wait'
           )


starttime = time.time()


Cfg = Default()


def docmd(clt: Client, txt: str) -> Event:
    "execute a command."
    cmd = Event()
    cmd.channel = ""
    cmd.orig = repr(clt)
    cmd.txt = txt
    clt.handle(cmd)
    cmd.wait()
    return cmd


def wait() -> None:
    "waiting loop."
    while True:
        time.sleep(1.0)
