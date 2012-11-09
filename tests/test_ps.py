import unittest

from muxpy import ps

class PsTest(unittest.TestCase):
    tests = [
        (' ', '\\ '),
        ('$', '\\$'),
        ('\'', '\\\''),
        ('\"', '\\\"'),
        ('\\', '\\\\'),
    ]

    def setUp(self):
        self.p = ps.Processes()

    def test_arg_escape(self):
        for escape, escapee in self.tests:
            self.assertEquals(self.p.make_safe_arg(escape), escapee)

        tests = zip(*self.tests)
        self.assertEquals(self.p.make_safe_arg('foo'.join(tests[0])), 'foo'.join(tests[1]))
        self.assertEquals(self.p.make_safe_arg(''.join(tests[0])), ''.join(tests[1]))

    def test_command_escape(self):
        self.assertEquals(self.p.make_safe_cmd('foo\0foo foo\0\'"$'), r'foo foo\ foo \'\"\$')
