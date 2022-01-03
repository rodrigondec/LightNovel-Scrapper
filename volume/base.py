import os
import uuid
import logging

from ebooklib import epub


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Volume:
    def __init__(self, title, number, novel):
        self.number = number
        self.title = title

        self.novel = novel
        self.chapters = []
        self.epub = None

    def __str__(self):
        return str(self.title)

    def add_chapter(self, chapter):
        logger.info(f"Chapter {chapter} added to queue!")
        self.chapters.append(chapter)
        chapter.novel = self.novel

    def process(self):
        logger.info("Processing chapters...")
        for chapter in self.chapters:
            logger.info(f"Processing chapter {chapter}...")
            chapter.process()
            logger.info(f"Chapter {chapter} done!")

    def build_chapters(self):
        logger.info("Building chapters epub...")
        chapters_epub = []
        for chapter in self.chapters:
            chapter_epub = epub.EpubHtml(
                title=chapter.title,
                file_name=f'{uuid.uuid4().hex}.xhtml',
                lang='en'
            )
            chapter_epub.content = chapter.build_chapter()
            self.epub.add_item(chapter_epub)
            self.epub.toc += (epub.Link(chapter_epub.file_name, chapter_epub.title, uuid.uuid4().hex),)
            chapters_epub.append(chapter_epub)
            logger.info(f"Epub for chapter {chapter} done!")
        return chapters_epub

    def build_epub(self):
        logger.info(f"build epub for {self}...")
        self.epub = epub.EpubBook()
        self.epub.set_title(f"{self.novel.title} - {self.title}")
        self.epub.set_identifier(uuid.uuid4().hex)
        self.epub.set_language('en')

        self.epub.add_item(epub.EpubNcx())
        self.epub.add_item(epub.EpubNav())
        self.epub.spine = ['Nav'] + self.build_chapters()

        st = 'p { margin-top: 1em; text-indent: 0em; } ' \
             'h1 {margin-top: 1em; text-align: center} ' \
             'h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;} ' \
             'h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;} ' \
             '.center { text-align: center; } ' \
             '.pagebreak { page-break-before: always; } '
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=st)
        self.epub.add_item(nav_css)

        novel_cache_path = self.novel.get_cache_path()
        epub_file_path = os.path.join(novel_cache_path, f'{self.epub.title}.epub')

        epub.write_epub(epub_file_path, self.epub, {})
        logger.info(f"Epub for volume {self} done!")
