import os
p = os.path

def get_profile_folder():
    user = p.expanduser('~')
    path = p.join(user, '.muxpy', 'profiles')
    return p.abspath(path)

def get_profile_path(profile, format):
    return p.join(get_profile_folder(), "%s.%s" % (profile, format))

if __name__ == '__main__':
    print get_profile_folder()
    print get_profile_path('testprof', 'json')
