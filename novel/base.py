import os
import abc

import logging
from bs4 import BeautifulSoup
from utils import request_page, get_cache_path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Novel(abc.ABC):
    def __init__(self, title, index_url, slug, **kwargs):
        self.title = title
        self.index_url = index_url
        self.slug = slug

        self.chosen_volumes = []

        self.index_soup = None

        self.volumes = []

    def __str__(self):
        return f"Novel {self.title}"

    @classmethod
    def from_data(cls, data):
        return cls(**data)

    def _is_volume_chosen(self, volume_number):
        if volume_number in self.chosen_volumes:
            return True
        return False

    def load_soup(self):
        logger.info("Loading index soup...")
        page = request_page(self.index_url)
        self.index_soup = BeautifulSoup(page.content, 'html.parser')

    def add_chosen_volume(self, volume_number):
        logger.info(f"volume {volume_number} added to queue!")
        self.chosen_volumes.append(volume_number)

    def add_volume(self, volume):
        logger.info(f"Volume {volume} added to {self}!")
        self.volumes.append(volume)
        volume.novel = self

    @abc.abstractmethod
    def load_volumes(self):
        raise Exception('Não pode ser chamado diretamente de Novel')

    def process(self):
        logger.info("Processing...")
        self.load_soup()
        self.load_volumes()

        for volume in self.volumes:
            logger.info(f"Processing volume {volume}...")
            volume.process()
            logger.info(f"volume {volume} processed!")
            volume.build_epub()

    def get_cache_path(self):
        cache_path = get_cache_path()
        cache_path = os.path.join(cache_path, self.slug)
        try:
            os.mkdir(cache_path)
        except FileExistsError:
            pass
        return cache_path
