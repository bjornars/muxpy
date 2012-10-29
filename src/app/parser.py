from .backend import Backend

class TmuxParser(object):
    def __init__(self, socket=None, backend=Backend):
        self.backend = backend(socket)

    def list_sessions(self):
        sessions = self.backend.list_sessions()
        return sessions

if __name__== '__main__':
    tmux = TmuxParser('/tmp/tmux-1000/default')
    print tmux.list_sessions()
