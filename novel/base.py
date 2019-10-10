import abc

import logging
import json
from bs4 import BeautifulSoup
from utils import request_page

logging.basicConfig(level=logging.INFO)


class Novel(abc.ABC):

    @classmethod
    def get_novels_data(cls):
        logging.info('Loading novels...')
        with open("novels.json", 'r') as file:
            return json.load(file)

    @classmethod
    def get_novel_data(cls, value, slug=True):
        for novel_data in cls.get_novels_data():
            if slug:
                novel_value = novel_data.get('slug')
            else:
                novel_value = novel_data.get('title')

            if value == novel_value:
                return novel_data
        return None

    def __init__(self, title, index_url):
        self.title = title
        self.index_url = index_url
        self.chosen_volumes = []

        self.index_soup = None

        self.volumes = []

    def __str__(self):
        return f"Novel {self.title}"

    @classmethod
    def from_data(cls, data):
        return cls(data.get('title'), data.get('index_url'))

    def _is_volume_chosen(self, volume_number):
        if volume_number in self.chosen_volumes:
            return True
        return False

    def load_soup(self):
        logging.info("Loading index soup...")
        page = request_page(self.index_url)
        self.index_soup = BeautifulSoup(page.content, 'html.parser')

    def add_chosen_volume(self, volume_number):
        logging.info(f"volume {volume_number} added to queue!")
        self.chosen_volumes.append(volume_number)

    @abc.abstractmethod
    def load_volumes(self):
        raise Exception('Não pode ser chamado diretamente de Novel')

    def process(self):
        logging.info("Processing...")
        self.load_soup()
        self.load_volumes()

        for volume in self.volumes:
            logging.info(f"Processing volume {volume}...")
            volume.process()
            logging.info(f"volume {volume} processed!")
            volume.build_epub(self.title)
