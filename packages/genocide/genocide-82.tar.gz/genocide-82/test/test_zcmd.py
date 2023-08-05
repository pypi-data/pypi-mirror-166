# This file is placed in the Public Domain.


"command"


import unittest


from genocide.hdl import Client, Commands, docmd
from genocide.obj import Object, get
from genocide.run import Cfg

evts = []
skip = ["cfg",]


param = Object()
param.cmd = [""]
param.cfg = ["nick=genocide", "server=localhost", "port=6699"]
param.fnd = ["log", "log txt==test", "config", "config name=genocide", "config server==localhost"]
param.flt = ["0", ""]
param.log = ["test1", "test2"]
param.mre = [""]
param.thr = [""]


class CLI(Client):

    def raw(self, txt):
        if Cfg.verbose:
            print(txt)


c = CLI()


def consume(events):
    fixed = []
    res = []
    for evt in events:
        evt.wait()
        fixed.append(evt)
    for evt in fixed:
        try:
            events.remove(evt)
        except ValueError:
            continue
    return res


class TestCommands(unittest.TestCase):

    def test_commands(self):
        cmds = sorted(Commands.cmd)
        for cmd in cmds:
            if cmd in skip:
                continue
            for ex in get(param, cmd, ""):
                evt = docmd(c, cmd + " " + ex)
                evts.append(evt)
        consume(evts)
        self.assertTrue(not evts)
