import unittest
import app.parser
import app.backend

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.p = app.parser.TmuxParser(backend=app.backend.MockBackend)

    def test_parse_list_sessions(self):
        self.assertListEqual(
                self.p.list_sessions(),
                [
                    dict(name='1',windows=2),
                    dict(name='muxpy',windows=3),
                ]
        )
