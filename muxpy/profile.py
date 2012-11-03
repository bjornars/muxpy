import os
p = os.path


def get_profile_path(profile, format):
    user = p.expanduser('~')
    path = p.join(user, '.muxpy', 'profiles', "%s.%s" % (profile, format))
    return p.abspath(path)


if __name__ == '__main__':
    print get_profile_path('testprof', 'json')
