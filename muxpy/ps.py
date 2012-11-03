import os
import re

from glob import glob


class Processes(object):
    def __init__(self):
        self.processes = {}

        # process inspection time
        for process in glob('/proc/*'):
            if not os.path.isdir(process):
                continue

            pid = os.path.split(process)[1]
            try:
                pid = int(pid)
            except ValueError:
                continue

            # find parent pid
            with open(os.path.join(process, 'status')) as f:
                status = f.read()
                parent = int(re.search('PPid:\t(\\d+)', status).group(1))

            # find cwd
            try:
                cwd = os.readlink(os.path.join(process, 'cwd'))
            except OSError:
                cwd = None

            # find command
            with open(os.path.join(process, 'cmdline')) as f:
                cmd = f.read().replace('\0', ' ')  # flakey!

            self.processes[pid] = dict(parent=parent, pid=pid, cwd=cwd, cmd=cmd, children=[])

        # fixup children pointers
        for k, v in self.processes.items():
            parent = v['parent']
            if parent in self.processes:
                self.processes[v['parent']]['children'].append(k)

    def __getitem__(self, item):
        return self.processes.__getitem__(item)

    def get(self, item):
        return self.processes.get(item)

if __name__ == '__main__':
    p = Processes()
    pid = os.getpid()
    while 1:
        print p[pid]
        pid = p[pid]['parent']
        if not pid:
            break
