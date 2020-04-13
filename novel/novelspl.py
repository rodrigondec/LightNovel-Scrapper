import logging
from time import sleep

from nerodia.browser import Browser

from novel.base import Novel
from volume.base import Volume
from chapter.novelspl import NovelsPLChapter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NovelsPLNovel(Novel):
    TYPE = 'novelspl'

    def load_volumes(self):
        logger.info("Loading volumes...")

        logger.info(f"Opening browser...")
        browser = Browser(browser='firefox')
        logger.info(f"Going to url...")
        browser.goto(self.index_url)

        browser.wait()
        logger.info(f"Click on last page...")
        browser.li({'class': 'last'}).js_click()

        logger.info(f"Getting chapters tbody...")
        chapter_links = [
            {
                'href': link.href,
                'text': link.text
            }
            for link in
            browser.tbody({'id': 'chapters'}).links()
        ]

        logger.info(f"Closing browser...")
        browser.close()

        logger.info(f"Reverse list...")
        chapter_links.reverse()

        logger.info(f"Creating volume...")
        volume = Volume()
        volume.title = self.title
        volume.number = 0

        logger.info(f"Iterating links...")
        for link in chapter_links:
            logger.info(f"Creating chapter...")
            volume.add_chapter(
                NovelsPLChapter(
                    url=link.get('href'),
                    title=link.get('text'),
                    novel=self
                )
            )

        self.volumes.append(volume)
        logger.info(f"Volume {volume} done!")


