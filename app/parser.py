import re

from .backend import Backend

RE_SESSIONS = re.compile(r"(?P<name>.*?): (?P<windows>\d*)")
class TmuxParser(object):
    def __init__(self, socket=None, backend=Backend):
        self.backend = backend(socket)

    def intify(self, dict_, keys):
        for k, v in list(dict_.iteritems()):
            if k in keys:
                dict_[k] = int(v)

    def list_sessions(self):
        sessions = filter(None, self.backend.list_sessions().split('\n'))

        matches = [RE_SESSIONS.search(each) for each in sessions]
        groups = [m.groupdict() for m in matches if m]

        for each in groups:
            self.intify(each, 'windows')

        return groups

if __name__== '__main__':
    tmux = TmuxParser(socket='/tmp/tmux-1000/default')
    print tmux.list_sessions()
