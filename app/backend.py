from .process import TmuxExecutor

class Backend(object):
    def __init__(self, socket):
        self.socket = socket
        self.tmux = TmuxExecutor(socket)

    def list_windows(self, session):
        return self.tmux('list-windows', '-t', session)

    def list_sessions(self):
        return self.tmux('list-sessions')
