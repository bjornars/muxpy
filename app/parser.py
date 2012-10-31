import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

from .backend import Backend

RE_SESSIONS = re.compile(r"^(?P<name>.*?): (?P<windows>\d*)")
RE_WINDOWS = re.compile(r"^(?P<number>\d*?): (?P<name>.*) \[\d+x\d+\] \[layout (?P<layout>.*?)$")


class ddict(dict):
    def __getattr__(self, item):
        return self.get(item, False)

    def __missing__(self, item):
        return False


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
        groups = [ddict(m.groupdict()) for m in matches if m]

        for each in groups:
            self.intify(each, 'windows')

        return groups

    def list_windows(self, session):
        windows = filter(None, self.backend.list_windows(session).split('\n'))
        matches = [RE_WINDOWS.search(each) for each in windows]
        groups = [ddict(m.groupdict()) for m in matches if m]

        for each in groups:
            self.intify(each, 'number')
            layout = each['layout']
            if layout.endswith(' (active)'):
                layout = layout[:-9]

            each['layout'] = layout[:-1]

        return groups

    def get_panes(self):
        RE_PANES = re.compile('[:.]')
        panes = filter(None, self.backend.list_panes().split('\n'))
        panes = map(lambda x: RE_PANES.split(x, 2)[:2], panes)
        panes.sort()

        pane_dict = defaultdict(dict)
        for session, windows in groupby(panes, itemgetter(0)):
            for window, panes in groupby(map(itemgetter(1), windows), itemgetter(0)):
                pane_dict[session][int(window)] = sum(1 for _ in panes)

        return dict(pane_dict)


if __name__ == '__main__':
    tmux = TmuxParser(socket='/tmp/tmux-1000/default')
    print tmux.list_sessions()
    print tmux.list_windows('muxpy')
