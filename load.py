#!/usr/bin/env python3
import concurrent.futures
import json
import logging
from logging.config import dictConfig
import os

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
    def __init__(self, name, api):
        self.name = name
        self.api = api
        self.path = 'data/{}.json'.format(self.name)

    @property
    def exists(self):
        """Determine if the resource has already been loaded."""
        return os.path.exists(self.path)

    def save(self):
        """Save JSON corresponding to the resource."""
        logger.info('Saving data for the [{}] resource.'.format(self.name))

        with open(self.path, 'w') as f:
            data = getattr(self.api, self.name).get()
            json.dump(data, f, indent=4, sort_keys=True)

        logger.info('Saved [{resource}] data to [{path}].'.format(resource=self.name, path=self.path))


if __name__ == '__main__':
    with open('settings.yml') as f:
        settings = yaml.load(f)

    mashape_api_root = settings['mashape_api']['root']
    mashape_api_key = settings['mashape_api']['key']

    headers = {'X-Mashape-Key': mashape_api_key}
    session = requests.Session()
    session.headers.update(headers)
    api = slumber.API(mashape_api_root, session=session)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        resources = [Resource(resource, api) for resource in settings['resources']]

        for resource in resources:
            # TODO: Add flag to force refresh (for use after a patch is released).
            if resource.exists:
                logger.info('Resource [{name}] found at [{path}].'.format(name=resource.name, path=resource.path))
            else:
                logger.info(
                    'Resource [{name}] not found. Saving to [{path}].'.format(
                        name=resource.name, path=resource.path
                    )
                )
                executor.submit(resource.save)
