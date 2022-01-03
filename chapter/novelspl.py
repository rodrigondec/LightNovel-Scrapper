import logging

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NovelsPLChapter(Chapter):
    def process(self):
        if self._loaded_from_cache:
            return

        logger.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self._soup.find('div', attrs={'class': 'article'})
        ps = chapter_content.find_all('p')

        ignored_ps = [
            'This chapter is updated by Novels.pl',
            'Click here and join our YouTube Channel',
            'Liked it? Take a second to support Novels on Patreon!',
            '', ' '
        ]

        ps = [p for p in ps if p.get_text().strip() not in ignored_ps]

        for p in ps:
            self._paragraphs.append(f"<p>{p.get_text()}</p>")

        self._save_cache()
