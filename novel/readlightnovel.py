import logging
import re

import bs4

from novel.base import Novel
from volume.base import Volume
# from chapter.mofumo import MofumoChapter

logging.basicConfig(level=logging.INFO)


class ReadLightNovelNovel(Novel):
    TYPE = 'readlightnovel'

    def load_volumes(self):
        logging.info("Loading volumes...")

        content = self.index_soup.find('div', attrs={'class', 'entry-content'})

        h3s = content.find_all('h3')

        titles = []
        for h3 in h3s:
            if (re.search(r"Volume", h3.get_text()) or
                    re.search(r"volume", h3.get_text()) or
                    re.search(r"\d+", h3.get_text())):
                titles.append(h3)

        for title in titles:
            assert isinstance(title, bs4.Tag)
            volume = Volume()
            volume.title = title.get_text()
            volume.number = re.search(r"\d+", volume.title).group()

            if not self._is_volume_chosen(volume.number):
                continue

            actual_div = title.find_next_sibling()
            assert isinstance(actual_div, bs4.Tag)
            while actual_div.find_next_sibling() and actual_div.find_next_sibling().name != 'h3':
                children = actual_div.next
                assert isinstance(children, bs4.Tag)
                if children.name == 'a':
                    volume.add_chapter(
                        MofumoChapter(
                            url=children.get('href'),
                            title=children.get_text().strip()
                        )
                    )

                actual_div = actual_div.find_next_sibling()

            self.volumes.append(volume)
            logging.info(f"Volume {volume} done!")
