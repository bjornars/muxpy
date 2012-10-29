from .process import TmuxExecutor

class Tmux(object):
    def __init__(self, socket):
        self.socket = socket
        self.tmux = TmuxExecutor(socket)

    def list_sessions(self):
        return self.tmux('list-sessions')
