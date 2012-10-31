import os
import sys

from collections import OrderedDict
from pprint import pprint

from app import profile, parser, formats, backend

def edit(p):
    prof =  profile.get_profile_path(p.profile, p.format)
    os.system('/etc/alternatives/editor "%s"' % prof)

def start(p):
    prof =  profile.get_profile_path(p.profile, p.format)
    if not os.path.isfile(prof):
        print >> sys.stderr, 'Cannot find profile %s' %  p.profile
        sys.exit(1)

    tmux = backend.Backend(socket=p.socket)

    with open(prof) as f:
        data = formats.parse(p.format, f.read())
    
    for session in data:
        tmux.create_session(session=session['name'], window=session['windows'][0]['name'])
           
        for window in session['windows'][1:]:
            tmux.new_window(window['name'])
        
        for window in session['windows']:
            tmux.select_window(window['name'])
            
            # make the required number of panes
            for _ in range(1, window['panes']):
                tmux.new_pane()

            tmux.select_layout(window['layout'])

    os.system('tmux -u2 -S %s attach' % p.socket)

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
