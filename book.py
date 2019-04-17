import logging
from ebooklib import epub
import uuid


logging.basicConfig(level=logging.INFO)


class Book:
    def __init__(self, title=None, number=None):
        self.number = number
        self.title = title
        self.chapters = []

    def __str__(self):
        return self.title

    def add_chapter(self, chapter):
        logging.info(f"Chapter {chapter} added to queue!")
        self.chapters.append(chapter)

    def process(self):
        logging.info("Processing chapters...")
        for chapter in self.chapters:
            logging.info(f"Processing chapter {chapter}...")
            chapter.process()
            logging.info(f"Chapter {chapter} done!")

    def build_chapters(self, book_epub):
        logging.info("Building chapters epub...")
        chapters_epub = []
        for chapter in self.chapters:
            chapter_epub = epub.EpubHtml(
                title=chapter.title,
                file_name=f'{uuid.uuid4().hex}.xhtml',
                lang='en'
            )
            chapter_epub.content = chapter.build_chapter()
            book_epub.add_item(chapter_epub)
            book_epub.toc += (epub.Link(chapter_epub.file_name, chapter_epub.title, uuid.uuid4().hex), )
            chapters_epub.append(chapter_epub)
            logging.info(f"Epub for chapter {chapter} done!")
        return chapters_epub
