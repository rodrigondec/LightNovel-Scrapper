import uuid
import logging

from ebooklib import epub


logging.basicConfig(level=logging.INFO)


class Volume:
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

    def build_chapters(self, volume_epub):
        logging.info("Building chapters epub...")
        chapters_epub = []
        for chapter in self.chapters:
            chapter_epub = epub.EpubHtml(
                title=chapter.title,
                file_name=f'{uuid.uuid4().hex}.xhtml',
                lang='en'
            )
            chapter_epub.content = chapter.build_chapter()
            volume_epub.add_item(chapter_epub)
            volume_epub.toc += (epub.Link(chapter_epub.file_name, chapter_epub.title, uuid.uuid4().hex),)
            chapters_epub.append(chapter_epub)
            logging.info(f"Epub for chapter {chapter} done!")
        return chapters_epub

    def build_epub(self, novel_title):
        logging.info(f"build epub for {self}...")
        volume_epub = epub.EpubBook()
        volume_epub.set_title(f"{novel_title} - {self.title}")
        volume_epub.set_identifier(uuid.uuid4().hex)
        volume_epub.set_language('en')

        volume_epub.add_item(epub.EpubNcx())
        volume_epub.add_item(epub.EpubNav())
        volume_epub.spine = ['Nav'] + self.build_chapters(volume_epub)

        st = 'p { margin-top: 1em; text-indent: 0em; } ' \
             'h1 {margin-top: 1em; text-align: center} ' \
             'h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;} ' \
             'h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;} ' \
             '.center { text-align: center; } ' \
             '.pagebreak { page-break-before: always; } '
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=st)
        volume_epub.add_item(nav_css)

        epub.write_epub(f'{volume_epub.title}.epub', volume_epub, {})
        logging.info(f"Epub for volume {self} done!")
