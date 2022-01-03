import logging

from novel.base import Novel
from volume.base import Volume
from chapter.novelspl import NovelsPLChapter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NovelsPLNovel(Novel):
    TYPE = 'novelspl'

    BASE_URL = 'https://www.novels.pl'

    def __init__(self, first_chapter_link, **kwargs):
        self.first_chapter_link = first_chapter_link

        super().__init__(**kwargs)

    def load_volumes(self):
        logger.info("Loading volumes...")

        logger.info(f"Creating volume...")
        volume = Volume(
            title='Volume único!',
            number=0
        )
        self.add_volume(volume)

        first_chapter = NovelsPLChapter(
            url=self.first_chapter_link
        )
        first_chapter.load_soup()

        current_chapter = first_chapter
        while current_chapter:
            article = current_chapter.chapter_soup.find('div', attrs={'class': 'article'})
            h4 = article.find('h4')
            current_chapter.title = h4.get_text().strip()

            volume.add_chapter(current_chapter)

            li_next = article.find('li', attrs={'class': 'next'})
            next_link = li_next.find('a').get('href')
            if next_link is None:
                current_chapter = None
                continue

            next_chapter = NovelsPLChapter(
                url=f"{self.BASE_URL}{next_link}"
            )
            next_chapter.load_soup()
            current_chapter = next_chapter

        logger.info(f"Volume {volume} done!")


