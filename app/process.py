import os
from subprocess import Popen, PIPE


class TmuxExecError(RuntimeError):
    pass


class TmuxExecutor(object):
    def __init__(self, socket=None):
        if not socket:
            socket = '/tmp/tmux-%s/default' % os.getuid()

        self.socket = socket
        self.cmd = ['/usr/bin/env', 'tmux', '-S', socket]

    def __call__(self, *command):
        cmd = self.cmd[:]
        cmd.append('--')
        cmd.extend(command)

        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        if p.returncode != 0:
            raise TmuxExecError(err)

        return out


if __name__ == '__main__':
    tmux = TmuxExecutor('/tmp/tmux-1000/default')
    print tmux('list-sessions'),
    print tmux('list-windows', '-t', 'muxpy'),
