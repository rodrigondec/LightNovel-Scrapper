import os

from uuid import uuid4
from time import sleep

import requests


DELAY = 1


def request_page(url):
    sleep(DELAY)

    headers = {
        'User-Agent': f'{uuid4()}',
    }
    request = requests.get(url, headers=headers)
    request.raise_for_status()
    return request


def get_cache_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(current_path, "cache")
    try:
        os.mkdir(cache_path)
    except FileExistsError:
        pass
    return cache_path
