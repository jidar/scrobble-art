import logging
from requests import api

#log = logging.getLogger('REST')
#log.addHandler(logging.StreamHandler(logging.info))

def get(url, params):
    r = api.get(url, params=params)
    return r
