from .process import TmuxExecutor

class Backend(object):
    def __init__(self, socket):
        self.socket = socket
        self.tmux = TmuxExecutor(socket)

    def list_windows(self, session):
        return self.tmux('list-windows', '-t', session)

    def list_panes(self):
        return self.tmux('list-panes', '-a')

    def list_sessions(self):
        return self.tmux('list-sessions')

    def create_session(self, session=None, window=None):
        args = ['new-session', '-d', '-x', '200', '-y', '200']
        if session:
            args.extend(['-s', session])
        if window:
            args.extend(['-n', window])

        return self.tmux(*args)

    def new_window(self, name):
        return self.tmux('new-window', '-d', '-n', name)

    def select_layout(self, layout):
        return self.tmux('select-layout', layout)

    def select_window(self, name):
        return self.tmux('select-window', '-t', name)

    def new_pane(self):
        self.tmux('split-window', '-h', '-l', '0')
        self.tmux('select-pane', '-L')

if __name__== '__main__':
    tmux = Backend('/tmp/tmux-1000/default')
    print tmux.list_panes('muxpy', 'bash')
