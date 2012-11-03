import unittest
import muxpy.parser
import muxpy.backend


class DotDefaultDictTest(unittest.TestCase):
    def test_defaults(self):
        d = muxpy.parser.ddict()
        self.assertFalse(d['foobar'])

    def test_dot(self):
        d = muxpy.parser.ddict()
        self.assertFalse(d.foobar)
        d.update(dict(foo='bar'))
        self.assertEquals(d.foo, 'bar')


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.p = muxpy.parser.TmuxParser()

    def test_parse_list_sessions(self):
        self.p.backend.list_sessions = lambda: \
"""1: 2 windows (created Sun Oct 28 18:12:25 2012) [151x41]
muxpy: 3 windows (created Sun Oct 28 12:45:07 2012) [151x41] (attached)
"""
        self.assertListEqual(
            self.p.list_sessions(),
            [
                dict(name='1', windows=2),
                dict(name='muxpy', windows=3),
            ]
        )

    def test_parse_borked_list_sessions(self):
        self.p.backend.list_sessions = lambda: \
"""foobar this is invalid
muxpy: 3 windows (created Sun Oct 28 12:45:07 2012) [151x41] (attached)
"""
        self.assertListEqual(
            self.p.list_sessions(),
            [dict(name='muxpy', windows=3)]
        )

    def test_parse_list_windows(self):
        self.p.backend.list_windows = lambda x: \
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

    def test_list_panes(self):
        self.p.backend.list_panes = lambda:  \
"""
1\t0\t0\t5957
muxpy\t0\t0\t2323
muxpy\t0\t1\t2437
muxpy\t0\t2\t13948
muxpy\t1\t0\t2624
muxpy\t1\t1\t4475
muxpy\t2\t0\t17702
muxpy\t2\t1\t5300
muxpy\t4\t0\t31118
muxpy\t4\t1\t20912
"""
        panes = self.p.get_panes(get_process_info=False)
        self.assertEquals(len(panes['1'][0]), 1)
        self.assertEquals(len(panes['muxpy'][0]), 3)
        self.assertEquals(len(panes['muxpy'][1]), 2)
        self.assertEquals(len(panes['muxpy'][2]), 2)
        self.assertEquals(len(panes['muxpy'][4]), 2)
