import os

import abc
import json
import logging

from bs4 import BeautifulSoup

from utils import request_page


logging.basicConfig(level=logging.INFO)


class Chapter:
    def __init__(self, url, title, novel):
        self.title = title
        self.url = url

        self.novel = novel
        self._soup = None
        self._paragraphs = []
        self._loaded_from_cache = False
        self._load_cache()

    def __str__(self):
        return self.title

    def load_soup(self):
        if self._soup is None:
            page = request_page(self.url)
            self._soup = BeautifulSoup(page.content, 'html.parser')

    def _load_cache(self):
        try:
            with open(self._cache_file_path, 'r') as file:
                data = json.load(file)
            self._paragraphs = data
            self._loaded_from_cache = True
            return True
        except FileNotFoundError:
            return False

    def _save_cache(self):
        with open(self._cache_file_path, 'w') as file:
            json.dump(self._paragraphs, file, indent=4)

    def process(self):
        raise NotImplementedError('Implemente o processamento do capitulo!')

    def build_chapter(self):
        self._paragraphs.insert(0, f"<h2>{self.title}</h2>")
        return ''.join(self._paragraphs)

    @property
    def _cache_folder_path(self):
        cache_path = self.novel.get_cache_path()
        cache_path = os.path.join(cache_path, 'chapters')
        try:
            os.mkdir(cache_path)
        except FileExistsError:
            pass
        return cache_path

    @property
    def _cache_file_path(self):
        cache_path = self._cache_folder_path
        return os.path.join(cache_path, f"{self.title}.json")
