import logging
from bs4 import BeautifulSoup
from utils import request_page


logging.basicConfig(level=logging.INFO)


class Chapter:
    def __init__(self, url=None, title=None):
        self.title = title
        self.url = url

        self.chapter_soup = None
        self.paragraphs = []

    def __str__(self):
        return self.title

    def load_soup(self):
        page = request_page(self.url)
        self.chapter_soup = BeautifulSoup(page.content, 'html.parser')

    def process(self):
        logging.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self.chapter_soup.find('div', attrs={'id': 'chapter-content'})
        ps = chapter_content.find_all('p')

        if len(ps) <= 10:
            ps = chapter_content.find_all('div')

        for p in ps:
            if p.get_text():
                self.paragraphs.append(f"<p>{p.get_text()}</p>")

    def build_chapter(self):
        self.paragraphs[0] = f"<h2>{self.title}</h2>"
        content = ''.join(self.paragraphs)
        self.paragraphs[0] = f"{self.title}"
        return content
