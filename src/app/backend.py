from .process import TmuxExecutor

class Backend(object):
    def __init__(self, socket):
        self.socket = socket
        self.tmux = TmuxExecutor(socket)

    def list_sessions(self):
        return self.tmux('list-sessions')

class MockBackend(Backend):
    def list_sessions(self):
        return """1: 2 windows (created Sun Oct 28 18:12:25 2012) [151x41]
muxpy: 3 windows (created Sun Oct 28 12:45:07 2012) [151x41] (attached)
"""
