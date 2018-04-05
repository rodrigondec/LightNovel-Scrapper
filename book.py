from ebooklib import epub
import uuid


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
