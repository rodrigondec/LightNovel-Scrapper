import logging
import re

from novel.base import Novel
from volume.base import Volume
from chapter.readlightnovel import ReadLightNovelChapter

logging.basicConfig(level=logging.INFO)


class ReadLightNovelNovel(Novel):
    TYPE = 'readlightnovel'

    def load_volumes(self):
        logging.info("Loading volumes...")

        accordion = self.index_soup.find(id='accordion')
        panels = accordion.find_all('div', attrs={'class', 'panel'})

        for panel in panels:
            heading_one = panel.find(id='headingOne')

            volume = Volume()
            volume.title = heading_one.get_text()
            try:
                volume.number = re.search(r"\d+", volume.title).group()
            except AttributeError:
                volume.number = 0

            tab_content = panel.find('div', attrs={'class', 'tab-content'})

            chapters_link = tab_content.find_all('a')

            for link in chapters_link:
                volume.add_chapter(
                    ReadLightNovelChapter(
                        url=link.get('href'),
                        title=link.get_text().strip(),
                        novel=self
                    )
                )

            self.volumes.append(volume)
            logging.info(f"Volume {volume} done!")
