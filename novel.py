from math import ceil
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
    db = {}

    @classmethod
    def load_novels(cls):
        logging.info('Loading novels...')
        with open("novels.json", 'r') as file:
            data = json.load(file)
            for novel_data in data:
                title = novel_data.get('title')
                has_books = novel_data.pop('has_books')

                if has_books:
                    novel = Novel.from_dict(novel_data)
                else:
                    novel = NovelBookLess.from_dict(novel_data)
                cls.db[title] = novel
        logging.info(cls.db)

    @classmethod
    def get_novel(cls, title):
        return cls.db.get(title)

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('title'), data.get('index_url'), data.get('has_books'))

    def __init__(self, title, index_url, skip_first):
        self.title = title
        self.skip_first = skip_first
        self.index_url = index_url
        self.chosen_books = []

        self.index_soup = None

        self.books = []

    def __str__(self):
        return f"Novel {self.title}"

    def load_soup(self):
        logging.info("Loading index soup...")
        page = request_page(self.index_url)
        self.index_soup = BeautifulSoup(page.content, 'html.parser')

    def add_chosen_book(self, book_number):
        logging.info(f"Book {book_number} added to queue!")
        self.chosen_books.append(book_number)

    def load_books(self):
        logging.info("Loading books...")

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
            logging.info("Book {} done!".format(book))

    def process(self):
        logging.info("Processing...")
        self.load_soup()
        self.load_books()

        for book in self.books:
            logging.info(f"Processing book {book}...")
            book.process()
            logging.info(f"Book {book} processed!")

        self.build_epubs()

    def build_epubs(self):
        logging.info("Building epubs...")
        for book in self.books:
            book_epub = epub.EpubBook()
            book_epub.set_title(f"{self.title} - {book.title}")
            book_epub.set_identifier(uuid.uuid4().hex)
            book_epub.set_language('en')

            chapters_epub = book.build_chapters(book_epub)

            book_epub.add_item(epub.EpubNcx())
            book_epub.add_item(epub.EpubNav())
            book_epub.spine = ['Nav'] + chapters_epub

            st = 'p { margin-top: 1em; text-indent: 0em; } ' \
                 'h1 {margin-top: 1em; text-align: center} ' \
                 'h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;} ' \
                 'h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;} ' \
                 '.center { text-align: center; } ' \
                 '.pagebreak { page-break-before: always; } '
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=st)
            book_epub.add_item(nav_css)

            epub.write_epub(f'{book_epub.title}.epub', book_epub, {})
            logging.info(f"Epub for book {book} done!")


class NovelBookLess(Novel):
    def load_books(self):
        logging.info("Loading books...")

        accordion = self.index_soup.find('div', attrs={'id': 'accordion'})
        panels = accordion.find_all('div', attrs={'class': 'panel'})

        assert len(panels) == 1

        panel = panels[0]

        logging.info("Calculating total of artificial books...")

        links = panel.find('div', attrs={'class': 'panel-body'}).find_all('a')

        qt_chapter_per_book = 150
        qt_books = ceil(len(links) / qt_chapter_per_book)

        logging.info(f"Total of artificial books is {qt_books}")

        for index in range(0, qt_books):
            book_number = index + 1
            book = Book()
            book.number = book_number

            book.number = str(book.number)
            if book.number not in self.chosen_books:
                continue

            initial_index = index * qt_chapter_per_book
            final_index = initial_index + qt_chapter_per_book
            if final_index > len(links):
                final_index = len(links) - 1

            book.title = f"book {book.number} - {final_index - initial_index} chapters"

            for link in links[initial_index:final_index]:
                book.add_chapter(Chapter(url=link.get('href'), title=link.get_text().strip()))

            self.books.append(book)
            logging.info("Book {} done!".format(book))