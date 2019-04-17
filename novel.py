import logging
import json
from bs4 import BeautifulSoup
from ebooklib import epub
import uuid
from utils import request_page
from chapter import Chapter
from book import Book

logging.basicConfig(level=logging.INFO)


class Novel:
    list = {}

    @classmethod
    def load_novels(cls):
        logging.info('Loading novels...')
        with open("novels.json", 'r') as file:
            data = json.load(file)
            for novel_data in data:
                title = novel_data['title']
                cls.list[title] = Novel.from_dict(novel_data)
        logging.info(cls.list)

    @classmethod
    def get_novel(cls, title):
        return cls.list.get(title)

    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['index_url'], data['has_books'], data['skip_first'])

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
        print("Loading index soup...")
        page = request_page(self.index_url)
        self.index_soup = BeautifulSoup(page.content, 'html.parser')

    def add_chosen_book(self, book_number):
        print("Book {} added to queue!".format(book_number))
        self.chosen_books.append(book_number)

    def load_books(self):
        print("Loading books...")
        if self.has_books:

            accordion = self.index_soup.find('div', attrs={'id': 'accordion'})
            panels = accordion.find_all('div', attrs={'class': 'panel'})

            for panel in panels:
                book = Book()
                book.number = int(panel.find('h4').find('span', attrs={'class': 'book'}).get_text())

                if self.skip_first:
                    book.number -= 1
                    if book.number == 0:
                        continue

                book.number = str(book.number)
                if book.number not in self.chosen_books:
                    continue

                book.title = panel.find('h4').find('span', attrs={'class': 'title'}).find('a').get_text().strip()

                links = panel.find('div', attrs={'class': 'panel-body'}).find_all('a')
                for link in links:
                    book.add_chapter(Chapter(url=link.get('href'), title=link.get_text().strip()))

                self.books.append(book)
                print("Book {} done!".format(book))

    def process(self):
        print("Processing...")
        self.load_soup()
        self.load_books()

        for book in self.books:
            print("Processing book {}...".format(book))
            book.process()
            print("Book {} processed!".format(book))

        self.build_epubs()

    def build_epubs(self):
        print("Building epubs...")
        for book in self.books:
            book_epub = epub.EpubBook()
            book_epub.set_title("{} - {}".format(self.title, book.title))
            book_epub.set_identifier(uuid.uuid4().hex)
            book_epub.set_language('en')

            chapters_epub = book.build_chapters(book_epub)

            book_epub.add_item(epub.EpubNcx())
            book_epub.add_item(epub.EpubNav())
            book_epub.spine = ['Nav'] + chapters_epub

            style = 'p { margin-top: 1em; text-indent: 0em; } ' \
                    'h1 {margin-top: 1em; text-align: center} ' \
                    'h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;} ' \
                    'h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;} ' \
                    '.center { text-align: center; } ' \
                    '.pagebreak { page-break-before: always; } '
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
            book_epub.add_item(nav_css)

            epub.write_epub('{}.epub'.format(book_epub.title), book_epub, {})
            print("Epub for book {} done!".format(book))
