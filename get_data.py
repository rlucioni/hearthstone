#!/usr/bin/env python3
import concurrent.futures
import json
import logging
from logging.config import dictConfig

import requests
import slumber
import yaml


dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(process)d [%(filename)s:%(lineno)d] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
})
logger = logging.getLogger(__name__)


with open('settings.yml') as f:
    settings = yaml.load(f)


mashape_api_root = settings['mashape_api']['root']
mashape_api_key = settings['mashape_api']['key']

headers = {'X-Mashape-Key': mashape_api_key}
session = requests.Session()
session.headers.update(headers)
api = slumber.API(mashape_api_root, session=session)


def save_data(resource):
    path = '/data/{filename}.json'.format(filename=resource)
    with open(path, 'w') as f:
        data = getattr(api, resource).get()
        json.dump(data, f, indent=4, sort_keys=True)


with concurrent.futures.ThreadPoolExecutor() as executor:
    for resource in ('info', 'cards', 'cardbacks'):
        executor.submit(save_data, resource)
