def run():
    import argparse
    import logging
    import os
    import sys
    import stat

    from . import commands
    from . import process

    default_socket = '/tmp/muxpy-%s/default' % os.getuid()

    p = argparse.ArgumentParser(prog='muxpy', description='manage tmux sessions')
    p.add_argument('-S', '--socket', default=default_socket, help='the tmux socket. defaults to ' + default_socket)
    p.add_argument('-v', '--verbose', default=0, action='count', help='set verbose mode. repeat up to 3 times')
    subp = p.add_subparsers(dest='command')

    helpp = subp.add_parser('help')
    helpp.add_argument('target', help='help on what?')

    createp = subp.add_parser('create', description='create a new session')
    createp.add_argument('profile', help='the profile name')
    createp.add_argument('--format', '-f', choices=['json'], default='json', help='profile format')

    editp = subp.add_parser('edit', description='edit a saved session')
    editp.add_argument('profile', help='the profile name')
    editp.add_argument('--format', '-f', choices=['json'], default='json', help='profile format')

    startp = subp.add_parser('start', description='start a saved session')
    startp.add_argument('profile', help='the profile name')
    startp.add_argument('--format', '-f', choices=['json'], default='json', help='profile format')

    subp.add_parser('kill', description='kill a socket')

    parsed = p.parse_args(sys.argv[1:])

    logging.basicConfig(format='')
    logger = logging.getLogger()
    levels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
    logger.setLevel(levels.get(parsed.verbose, 3))

    if parsed.command == 'help':
        args = [parsed.target, '--help']
        p.parse_args(args)
        sys.exit(1)

    def err_out(msg):
        logger.error(msg)
        p.print_help()
        sys.exit(1)

    if parsed.command == 'create':
        try:
            s = os.stat(parsed.socket)
        except OSError:
            err_out('%s does not exist' % parsed.socket)

        if not stat.S_ISSOCK(s.st_mode):
            err_out('%s is not a socket' % parsed.socket)

    try:
        if parsed.command == 'start':
            commands.start(parsed)
        elif parsed.command == 'create':
            commands.create(parsed)
        elif parsed.command == 'edit':
            commands.edit(parsed)
        elif parsed.command == 'kill':
            commands.kill(parsed)
    except process.TmuxExecError as e:
        logger.error(e.message)

    sys.exit(0)
