import json
from bs4 import BeautifulSoup
import requests
from time import sleep
from ebooklib import epub
import uuid


BASE_URL = 'http://www.wuxiaworld.com'
DELAY = 0


def request_page(url):
    sleep(DELAY)
    return requests.get(BASE_URL + url)


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
            self.paragraphs.append(p.get_text())

    def build_chapter(self):
        self.paragraphs[0] = "<h1>{}</h1>".format(self.title)
        content = '<br /><br />'.join(self.paragraphs)
        self.paragraphs[0] = "{}".format(self.title)
        return content


class Book:
    def __init__(self, title=None, number=None):
        self.number = number
        self.title = title
        self.chapters = []

    def __str__(self):
        return self.title

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def process(self):
        for chapter in self.chapters:
            chapter.process()

    def build_chapters(self, book_epub):
        chapters_epub = []
        for chapter in self.chapters:
            chapter_epub = epub.EpubHtml(
                title=chapter.title,
                file_name='{}.xhtml'.format(uuid.uuid4().hex),
                lang='en'
            )
            chapter_epub.content = chapter.build_chapter()
            book_epub.add_item(chapter_epub)
            book_epub.toc += (epub.Link(chapter_epub.file_name, chapter_epub.title, uuid.uuid4().hex), )
            chapters_epub.append(chapter_epub)

        return chapters_epub


class Novel:
    list = {}

    @staticmethod
    def load_novels():
        with open("novels.json", 'r') as file:
            data = json.load(file)
            for novel in data['novels']:
                title = novel['title']
                index_url = novel['index_url']
                has_books = novel['has_books']
                skip_first = novel['skip_first']
                Novel.list[title] = Novel(title, index_url, has_books, skip_first)

    @staticmethod
    def get_novel(name):
        return Novel.list[name]

    def __init__(self, title, index_url, has_books, skip_first):
        self.title = title
        self.has_books = has_books
        self.skip_first = skip_first
        self.index_url = index_url
        self.chosen_books = []

        self.index_soup = None

        self.books = []

    def __str__(self):
        return "Novel {}".format(self.title)

    def load_soup(self):
        page = request_page(self.index_url)
        self.index_soup = BeautifulSoup(page.content, 'html.parser')

    def add_chosen_book(self, book_number):
        self.chosen_books.append(book_number)

    def load_books(self):
        if self.has_books:

            accordion = self.index_soup.find('div', attrs={'id': 'accordion'})
            panels = accordion.find_all('div', attrs={'class': 'panel'})

            for panel in panels:
                book = Book()
                book.number = int(panel.find('h4').find('span', attrs={'class': 'book'}).get_text())
                if self.skip_first:
                    book.number -= 1
                    book.number = str(book.number)
                    if book.number == "0":
                        continue

                if book.number not in self.chosen_books:
                    continue

                book.title = panel.find('h4').find('span', attrs={'class': 'title'}).find('a').get_text().strip()

                links = panel.find('div', attrs={'class': 'panel-body'}).find_all('a')
                for link in links:
                    book.add_chapter(Chapter(url=link.get('href'), title=link.get_text().strip()))

                self.books.append(book)

    def process(self):
        self.load_soup()
        self.load_books()

        for book in self.books:
            book.process()

        self.build_epubs()

    def build_epubs(self):
        for book in self.books:
            book_epub = epub.EpubBook()
            book_epub.set_title("{} - {}".format(self.title, book.title))
            book_epub.set_identifier(uuid.uuid4().hex)
            book_epub.set_language('en')

            chapters_epub = book.build_chapters(book_epub)

            book_epub.add_item(epub.EpubNcx())
            book_epub.add_item(epub.EpubNav())
            book_epub.spine = ['Nav'] + chapters_epub

            style = 'BODY {color: white;}'
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
            book_epub.add_item(nav_css)

            epub.write_epub('{}.epub'.format(book_epub.title), book_epub, {})

Novel.load_novels()
c = Novel.get_novel('Coiling Dragon')
assert isinstance(c, Novel)
c.add_chosen_book("1")
c.add_chosen_book("2")
c.process()
