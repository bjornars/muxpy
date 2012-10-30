import os
p = os.path

def get_profile_path(profile, format):
    return p.abspath(p.join(p.expanduser('~'), '.muxpy', 'profiles', "%s.%s" % (profile, format)))

if __name__== '__main__':
    print get_profile_path('testprof', 'json')
