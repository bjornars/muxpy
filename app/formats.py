import json

def format(file_format, data):
    if file_format == 'json':
        return json.dumps(data, indent=4)
    else:
        raise NotImplementedError('there is no support yet for %s' % file_format)
