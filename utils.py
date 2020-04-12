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
