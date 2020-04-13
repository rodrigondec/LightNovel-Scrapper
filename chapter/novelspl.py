import logging

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NovelsPLChapter(Chapter):
    def process(self):
        self.pre_process()

        if self.paragraphs:
            logger.info(f"Found cache! skipping for chapter {self}...")
            return

        logger.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self.chapter_soup.find('div', attrs={'class': 'article'})
        ps = chapter_content.find_all('p')

        ignored_ps = [
            'This chapter is updated by Novels.pl',
            'Click here and join our YouTube Channel',
            'Liked it? Take a second to support Novels on Patreon!',
            '', ' '
        ]

        ps = [p for p in ps if p.get_text().strip() not in ignored_ps]

        for p in ps:
            self.paragraphs.append(f"<p>{p.get_text()}</p>")

        self.post_process()
