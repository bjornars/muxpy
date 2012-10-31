import os
import sys

from collections import OrderedDict
from pprint import pprint

from app import profile, parser, formats

def edit(p):
    prof =  profile.get_profile_path(p.profile, p.format)
    os.system('/etc/alternatives/editor "%s"' % prof)


def start(*args):
    print 'start', args

def create(p):
    format = p.format
    prof =  profile.get_profile_path(p.profile, p.format)
    pname, fname = os.path.split(prof)
    if not os.path.isdir(pname):
        os.makedirs(pname)
    
    data = []

    tmux = parser.TmuxParser(p.socket)
    sessions = tmux.list_sessions()
    panes = tmux.get_panes()

    for session in sessions:
        session_data = OrderedDict(name=session.name)
        windows = tmux.list_windows(session.name)
        for window in windows:
            window['panes'] = panes[session['name']][window['number']]

        session_data['windows'] = windows
        data.append(session_data)
    
    formatted = formats.format(p.format, data)
    with open(prof, 'w') as f:
        f.write(formatted)

    print 'made profile, %d sessions with total %d windows' % (len(data), sum(len(x['windows']) for x in data))
