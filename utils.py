from time import sleep
import requests


DELAY = 1


def request_page(url):
    sleep(DELAY)
    return requests.get(url)
