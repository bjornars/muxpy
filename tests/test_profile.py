import unittest

from app import profile

class TestProfile(unittest.TestCase):
    def test_get_profile(self):
        profile.p.expanduser = lambda x: "/foobar"
        self.assertEquals(
                profile.get_profile_path('baz', 'quux'),
                '/foobar/.muxpy/profiles/baz.quux')
