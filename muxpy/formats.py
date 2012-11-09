import json

import logging
logger = logging.getLogger()

def parse(file_format, data):
    if file_format == 'json':
        logger.info('reading %d bytes as json', len(data))
        return json.loads(data)
    else:
        raise NotImplementedError('there is no support yet for %s' % file_format)


def format(file_format, data):
    if file_format == 'json':
        json_data = json.dumps(data, indent=4)
        logger.info('dumping %d bytes as json', len(json_data))
        return json_data
    else:
        raise NotImplementedError('there is no support yet for %s' % file_format)
