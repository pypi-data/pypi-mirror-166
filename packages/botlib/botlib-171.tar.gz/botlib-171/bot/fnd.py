# This file is placed in the Public Domain.


"find"


import time


from .dbs import find
from .obj import printable
from .utl import elapsed, fntime, gettypes
from .wdr import Wd


def fnd(event):
    "return list of matching objects."
    if not event.args:
        res = ",".join(
            sorted({x.split(".")[-1].lower() for x in gettypes(Wd.workdir)}))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    bot = event.bot()
    otype = event.args[0]
    res = list(find(otype, event.gets))
    if bot.cache:
        if len(res) > 3:
            bot.extend(event.channel, [x[1].txt for x in res])
            bot.say(event.channel, "%s left in cache, use !mre to show more" % bot.cache.size())
            return
    _nr = 0
    for _fn, obj in res:
        txt = "%s %s %s" % (
                            str(_nr),
                            printable(obj, event.sets.keys, event.toskip, plain=True),
                            elapsed(time.time()-fntime(_fn))
                           )
        _nr += 1
        event.reply(txt)
    if not _nr:
        event.reply("no result")
