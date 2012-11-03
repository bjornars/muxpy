import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

from .backend import Backend
from .ps import Processes

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
        panes = filter(None, self.backend.list_panes().split('\n'))
        panes = map(lambda x: x.split('\t'), panes)
        panes.sort()
        pane_dict = defaultdict(dict)

        processes = Processes()

        def get_pane_info(pid):
            process = processes[pid]
            if len(process['children']) != 1:
                return {}

            child = processes[process['children'][0]]
            return dict(cwd=child['cwd'], cmd=child['cmd'])

        for session, windows in groupby(panes, itemgetter(0)):
            windows = [x[1:] for x in windows]

            for window, panes in groupby(windows, itemgetter(0)):
                pane_dict[session][int(window)] = [get_pane_info(int(each[2])) for each in panes]

        return dict(pane_dict)


if __name__ == '__main__':
    tmux = TmuxParser(socket='/tmp/tmux-1000/default')
    print tmux.list_sessions()
    print tmux.list_windows('muxpy')
