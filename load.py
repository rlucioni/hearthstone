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


class Resource:
    """Utility class representing an API resource."""
    def __init__(self, resource, api):
        self.resource = resource
        self.api = api

    def save(self):
        """Save JSON corresponding to the resource."""
        logger.info('Saving data for the [{}] resource.'.format(self.resource))

        path = 'data/{}.json'.format(self.resource)
        with open(path, 'w') as f:
            data = getattr(self.api, self.resource).get()
            json.dump(data, f, indent=4, sort_keys=True)

        logger.info('Saved [{resource}] data to [{path}].'.format(resource=self.resource, path=path))


if __name__ == '__main__':
    with open('settings.yml') as f:
        settings = yaml.load(f)

    mashape_api_root = settings['mashape_api']['root']
    mashape_api_key = settings['mashape_api']['key']

    headers = {'X-Mashape-Key': mashape_api_key}
    session = requests.Session()
    session.headers.update(headers)
    api = slumber.API(mashape_api_root, session=session)

    resources = [Resource(resource, api) for resource in ('info', 'cards', 'cardbacks')]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for resource in resources:
            executor.submit(resource.save)

    logger.info('Resource saving complete.')
