from .tmux import Tmux

class TmuxParser(object):
    def __init__(self, socket):
        self.tmux = Tmux(socket)

    def list_sessions(self):
        sessions = self.tmux.list_sessions()
        print sessions
