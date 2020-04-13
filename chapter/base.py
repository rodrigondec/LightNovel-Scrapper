import os

import abc
import json
import logging

from bs4 import BeautifulSoup

from utils import request_page


logging.basicConfig(level=logging.INFO)


class Chapter(abc.ABC):
    def __init__(self, url=None, title=None, novel=None):
        self.title = title
        self.url = url

        self.novel = novel
        self.chapter_soup = None
        self.paragraphs = []

    def __str__(self):
        return self.title

    def load_soup(self):
        if self.chapter_soup is None:
            page = request_page(self.url)
            self.chapter_soup = BeautifulSoup(page.content, 'html.parser')

    def pre_process(self):
        try:
            with open(self.get_cache_file_path(), 'r') as file:
                data = json.load(file)
            self.paragraphs = data
        except FileNotFoundError:
            pass

    @abc.abstractmethod
    def process(self):
        raise Exception('Não pode ser chamado diretamente de Chapter')

    def post_process(self):
        try:
            with open(self.get_cache_file_path(), 'w') as file:
                json.dump(self.paragraphs, file, indent=4)
        except FileNotFoundError as e:
            os.mkdir(self.get_cache_path())
            self.post_process()

    def build_chapter(self):
        self.paragraphs.insert(0, f"<h2>{self.title}</h2>")
        return ''.join(self.paragraphs)

    def get_cache_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        cache_path = os.path.join(current_path, "cache")
        if self.novel:
            cache_path = os.path.join(cache_path, self.novel.slug)
        try:
            os.mkdir(cache_path)
        except FileExistsError:
            pass
        return cache_path

    def get_cache_file_path(self):
        cache_path = self.get_cache_path()
        return os.path.join(cache_path, f"{self.title}.json")
