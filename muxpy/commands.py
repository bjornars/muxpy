import logging
import os
import sys

from collections import OrderedDict
from itertools import count

from . import profile, parser, formats, backend

logger = logging.getLogger()

def edit(p):
    prof = profile.get_profile_path(p.profile, p.format)
    cmd = '/etc/alternatives/editor "%s"' % prof

    logger.info('executing %s', cmd)
    os.system(cmd)


def start(p):
    prof = profile.get_profile_path(p.profile, p.format)
    if not os.path.isfile(prof):
        print >> sys.stderr, 'Cannot find profile %s' % p.profile
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
            for index, pane in enumerate(window['panes']):
                if index > 0:
                    tmux.new_pane()

                if pane and 'cwd' in pane:
                    tmux.send_keys('cd %s\n' % pane['cwd'])

                if pane and 'cmd' in pane:
                    tmux.send_keys('%s\n' % pane['cmd'])

            tmux.select_layout(window['layout'])

    attach(p)


def create(p):
    prof = profile.get_profile_path(p.profile, p.format)
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

        unique_windows = []
        for window in windows:
            # make sure the window name is unique, or else tmux will weep loudly
            if not window['name'] in unique_windows:
                unique_windows.append(window['name'])
            else:
                for x in count():
                    new_window = "%s_%d" % (window['name'], x)
                    if new_window not in unique_windows:
                        break
                unique_windows.append(new_window)
                window['name'] = new_window

            window['panes'] = panes[session['name']][window['number']]

        session_data['windows'] = windows
        data.append(session_data)

    formatted = formats.format(p.format, data)

    with open(prof, 'w') as f:
        f.write(formatted)

    print 'made profile, %d sessions with total %d windows' % (len(data), sum(len(x['windows']) for x in data))

def attach(p):
    cmd = 'tmux -u2 -S %s attach' % p.socket
    logger.info('executing %s', cmd)
    os.system(cmd)

def kill(p):
    tmux = backend.Backend(socket=p.socket)
    tmux.kill_server()
    os.unlink(p.socket)
    print 'killed tmux at %s' % p.socket

def list(p):
    from glob import glob
    profile_formats = formats.get_formats()
    files = glob(os.path.join(profile.get_profile_folder(), '*'))
    files = [os.path.splitext(f) for f in files]
    files = [(path, ext[1:]) for path, ext in files]
    files = [os.path.split(path) + (ext,) for path, ext in files if ext in profile_formats]

    if files:
        print 'profile\t\tformat'
        print '-' * 20

        for _, profile_name, format in files:
            print "%s\t\t%s" % (profile_name, format)
    else:
        print 'there are no saved profiles in %s' % profile.get_profile_folder()
