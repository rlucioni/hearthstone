import logging
from logging.config import dictConfig
from urllib.parse import urljoin

import requests
import yaml


# Configure logging.
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
logger = logging.getLogger()


with open('settings.yml') as f:
    settings = yaml.load(f)


mashape_api_root = settings['mashape_api']['root']
mashape_api_key = settings['mashape_api']['key']


def get_all_cards():
    """
    Data is a dict of lists. The keys are card set names (e.g., 'Mean Streets of Gadgetzan').
    The card set lists may contain minions, spells, enchantments, and more.

    >>> data['Mean Streets of Gadgetzan'][0]
    {
        'artist': 'Paul Mafayon',
        'type': 'Enchantment',
        'locale': 'enUS',
        'text': 'Increased Attack.',
        'cardSet': 'Mean Streets of Gadgetzan',
        'name': 'Cut Off',
        'cardId': 'CFM_658e',
        'playerClass': 'Neutral'
    }
    """
    # TODO: Use https://pypi.python.org/pypi/slumber/0.7.1
    all_cards_url = urljoin(mashape_api_root, 'cards')
    headers = {
        'X-Mashape-Key': mashape_api_key,
    }
    response = requests.get(all_cards_url, headers=headers)
    return response.json()
