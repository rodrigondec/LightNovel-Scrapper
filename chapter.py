from bs4 import BeautifulSoup
from utils import request_page


class Chapter:
    def __init__(self, url=None, title=None):
        self.title = title
        self.url = url

        self.chapter_soup = None
        self.paragraphs = []

    def load_soup(self):
        page = request_page(self.url)
        self.chapter_soup = BeautifulSoup(page.content, 'html.parser')

    def process(self):
        self.load_soup()

        ps = self.chapter_soup.find('div', attrs={'class': 'content'}).find_all('p')

        for p in ps:
            self.paragraphs.append("<p>{}</p>".format(p.get_text()))

    def build_chapter(self):
        self.paragraphs[0] = "<h3>{}</h3>".format(self.title)
        content = ''.join(self.paragraphs)
        self.paragraphs[0] = "{}".format(self.title)
        return content
