from subprocess import Popen, PIPE

class TmuxExecError(RuntimeError):
    pass

class Tmux(object):
    def __init__(self, socket):
        self.socket = socket
        self.cmd = ['/usr/bin/env', 'tmux', '-S', socket]
    
    def run(self, command):
        p = Popen(self.cmd + [command], stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        if p.returncode != 0:
            raise TmuxExecError(err)
        
        return out

if __name__== '__main__':
    print Tmux('/tmp/tmux-1000/default').run('listxsessions')
