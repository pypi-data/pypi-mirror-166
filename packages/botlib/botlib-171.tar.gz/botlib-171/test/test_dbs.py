# This file is placed in the Public Domain.
# pylint: disable=E1101,E0611,C0116,C0413,C0411,W0406,R0903


"database"


import os
import unittest


from bot.dbs import fns, hook, last
from bot.hdl import Handler
from bot.jsn import dumps, loads, save
from bot.obj import Object
from bot.utl import cdir
from bot.wdr import getpath


class Composite(Object):

    "composite test class"

    def __init__(self):
        super().__init__()
        self.dbs = Handler()


class TestDbs(unittest.TestCase):

    "database test class."

    def test_cdir(self):
        cdir(".test")
        self.assertTrue(os.path.exists(".test"))

    def test_composite(self):
        com1 = Composite()
        com2 = loads(dumps(com1))
        self.assertEqual(type(com2.dbs), type({}))

    def test_fns(self):
        obj = Object()
        save(obj)
        self.assertTrue("Object" in fns(getpath("bot.obj.Object"))[0])

    def test_hook(self):
        obj = Object()
        obj.key = "value"
        pth = save(obj)
        oobj = hook(pth)
        self.assertEqual(oobj.key, "value")

    def test_last(self):
        oobj = Object()
        oobj.key = "value"
        save(oobj)
        last(oobj)
        self.assertEqual(oobj.key, "value")
