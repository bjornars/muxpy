import mock
import os
import tempfile
import unittest

from muxpy import process


class ProcessTest(unittest.TestCase):
    def test_process_execution(self):
        self.t = process.TmuxExecutor()
        self.t._execute = mock.Mock()
        self.t('foobar')

        self.t._execute.assert_called_once_with(
            ['/usr/bin/env', 'tmux', '-S', '/tmp/tmux-1000/default', '--', 'foobar']
        )

    def test_init_creates_directory_for_socket(self):
        socket_dir = tempfile.mktemp()
        socket_file = os.path.join(socket_dir, 'foobar')
        self.assertFalse(os.path.isdir(socket_dir))

        self.t = process.TmuxExecutor(socket=socket_file)

        self.assertTrue(os.path.isdir(socket_dir))
        os.rmdir(socket_dir)
