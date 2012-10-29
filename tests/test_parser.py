import unittest
import app.parser
import app.backend
import mock

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
