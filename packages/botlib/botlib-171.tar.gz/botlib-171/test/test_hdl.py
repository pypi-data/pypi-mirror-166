# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"bus"


import unittest


from bot.clt import Client
from bot.evt import Event
from bot.tbl import Bus


def test():
    pass


class MyClient(Client):

    gotcha = False

    def raw(self, txt):
        self.gotcha = True


class TestBus(unittest.TestCase):

    def test_construct(self):
        bus = Bus()
        self.assertEqual(type(bus), Bus)

    def test_add(self):
        bus = Bus()
        clt = MyClient()
        bus.add(clt)
        self.assertTrue(clt in bus.objs)

    def test_announce(self):
        bus = Bus()
        clt = MyClient()
        bus.add(clt)
        bus.announce("test")
        self.assertTrue(clt.gotcha)

    def test_byorig(self):
        bus = Bus()
        clt = MyClient()
        self.assertEqual(bus.byorig(repr(clt)), clt)

    def test_say(self):
        bus = Bus()
        clt = MyClient()
        bus.add(clt)
        bus.say(repr(clt), "#test", "test")
        self.assertTrue(clt.gotcha)



class TestEvent(unittest.TestCase):

    def testconstructor(self):
        evt = Event()
        self.assertEqual(type(evt), Event)
