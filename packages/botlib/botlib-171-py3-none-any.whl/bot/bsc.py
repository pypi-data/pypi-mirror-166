# This file is placed in the Public Domain.


"basic"


import time


from .hdl import Commands
from .run import starttime
from .utl import elapsed


def cmd(event):
    "show commands."
    event.reply(",".join(sorted(Commands.cmds)))


def upt(event):
    "show uptime."
    event.reply(elapsed(time.time()-starttime))
