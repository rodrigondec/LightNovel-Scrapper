from time import sleep
import requests


BASE_URL = 'http://www.wuxiaworld.com'
DELAY = 1


def request_page(url):
    sleep(DELAY)
    return requests.get(BASE_URL + url)
