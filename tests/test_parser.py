import unittest
import app.parser
import app.backend
import mock

class DotDefaultDictTest(unittest.TestCase):
    def test_defaults(self):
        d = app.parser.ddict()
        self.assertFalse(d['foobar'])

    def test_dot(self):
        d = app.parser.ddict()
        self.assertFalse(d.foobar)
        d.update(dict(foo='bar'))
        self.assertEquals(d.foo, 'bar')


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.p = app.parser.TmuxParser()

    def test_parse_list_sessions(self):
        self.p.backend.list_sessions = lambda: \
"""1: 2 windows (created Sun Oct 28 18:12:25 2012) [151x41]
muxpy: 3 windows (created Sun Oct 28 12:45:07 2012) [151x41] (attached)
"""
        self.assertListEqual(
            self.p.list_sessions(),
            [
                dict(name='1',windows=2),
                dict(name='muxpy',windows=3),
            ]
        )

    def test_parse_borked_list_sessions(self):
        self.p.backend.list_sessions = lambda: \
"""foobar this is invalid
muxpy: 3 windows (created Sun Oct 28 12:45:07 2012) [151x41] (attached)
"""
        self.assertListEqual(
            self.p.list_sessions(),
            [dict(name='muxpy',windows=3)]
        )

    def test_parse_list_windows(self):
        self.p.backend.list_windows= lambda x: \
"""0: dev [151x41] [layout e12a,151x41,0,0{70x41,0,0,80x41,71,0[80x21,71,0,80x19,71,22]}] (active)
1: man [151x41] [layout cb5b,151x41,0,0{75x41,0,0,75x41,76,0}]
2: bash [151x41] [layout bfde,151x41,0,0]
"""

        self.assertListEqual(
            self.p.list_windows(None),
            [
                dict(number=0, name='dev', layout='e12a,151x41,0,0{70x41,0,0,80x41,71,0[80x21,71,0,80x19,71,22]}'),
                dict(number=1, name='man', layout='cb5b,151x41,0,0{75x41,0,0,75x41,76,0}'),
                dict(number=2, name='bash', layout='bfde,151x41,0,0'),
            ]
        )

