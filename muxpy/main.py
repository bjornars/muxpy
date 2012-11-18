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

    subp = p.add_subparsers(dest='command', title='available subcommands')

    help = {
        'create': dict(
            help='create a new profile from an existing session',
            description='create a new session'),
        'edit': dict(
            help='edit a saved session',
            description='edit a profile manually'),
        'start': dict(
            description='start a saved session',
            help='start a saved profile'),
        'attach': dict(
            description='attach to a socket',
            help='attach to an existing tmux session'),
        'kill': dict(
            description='kill a socket',
            help='kill an existing tmux session'),
    }

    def add_profile(p):
        p.add_argument('profile', help='the profile name')
        p.add_argument('-f', '--format', choices=['json'], default='json', help='profile format')

    def add_parser(p, command):
        return p.add_parser(command, **help[command])

    helpp = subp.add_parser('help')
    helpp.add_argument('target', help='help on what?', nargs='?')

    createp = add_parser(subp, 'create')
    add_profile(createp)

    editp = add_parser(subp, 'edit')
    add_profile(editp)

    startp = add_parser(subp, 'start')
    add_profile(startp)

    add_parser(subp, 'attach')
    add_parser(subp, 'kill')

    if len(sys.argv) == 1:
        sys.argv.append('help')

    parsed = p.parse_args(sys.argv[1:])

    logging.basicConfig(format='')
    logger = logging.getLogger()
    levels = {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
    logger.setLevel(levels.get(parsed.verbose, 3))
#     logger.warning('logging set to %s' % logging.getLevelName(levels.get(parsed.verbose, 3)))

    if parsed.command == 'help':
        args = ['--help']
        if parsed.target:
            args.insert(0, parsed.target)

        p.parse_args(args)
        sys.exit(1)

    def err_out(msg):
        logger.error(msg)
        p.print_help()
        sys.exit(1)

    if parsed.command in  ['create', 'attach']:
        try:
            s = os.stat(parsed.socket)
        except OSError:
            err_out('%s does not exist' % parsed.socket)

        if not stat.S_ISSOCK(s.st_mode):
            err_out('%s is not a socket' % parsed.socket)

    try:
        command = getattr(commands, parsed.command)
        if command:
            command(parsed)

    except process.TmuxExecError as e:
        logger.error(e.message)

    sys.exit(0)
