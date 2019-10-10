import logging
import re

import bs4

from novel.base import Novel
from volume.base import Volume
from chapter.wandering import WanderingChapter

logging.basicConfig(level=logging.INFO)


class WanderingNovel(Novel):

    def load_volumes(self):
        logging.info("Loading volumes...")

        content = self.index_soup.find('div', attrs={'class', 'entry-content'})

        ps = content.find_all('p')
        volume = Volume()
        volume.number = 1

        for p in ps:
            children = p.next
            if (re.search(r"hapter", p.get_text()) or
                    re.search(r"rologue", p.get_text()) or
                    re.search(r"\d+", p.get_text())) and children.name == 'a':
                volume.add_chapter(
                    WanderingChapter(
                        url=children.get('href'),
                        title=children.get_text().strip()
                    )
                )

        volume.title = f'{volume.chapters[0].title} - {volume.chapters[-1].title}'
        self.volumes.append(volume)
        logging.info(f"Volume {volume} done!")
