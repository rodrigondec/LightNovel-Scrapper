import logging
from math import ceil

from novel.base import Novel
from volume.base import Volume
from chapter.wuxiaworld import WuxiaChapter

logging.basicConfig(level=logging.INFO)


class WuxiaWorldNovel(Novel):
    TYPE = 'wuxiaworld'

    BASE_URL = 'http://www.wuxiaworld.com'

    def __init__(self, skip_first, **kwargs):
        self.skip_first = skip_first

        super().__init__(**kwargs)

    def load_volumes(self):
        logging.info("Loading volumes...")

        accordion = self.index_soup.find('div', attrs={'id': 'accordion'})
        panels = accordion.find_all('div', attrs={'class': 'panel'})

        for panel in panels:
            volume = Volume()
            volume.number = int(panel.find('h4').find('span', attrs={'class': 'book'}).get_text())
            self.add_volume(volume)

            if self.skip_first:
                volume.number -= 1
                if volume.number == 0:
                    continue

            volume.number = str(volume.number)

            volume.title = panel.find('h4').find('span', attrs={'class': 'title'}).find('a').get_text().strip()

            links = panel.find('div', attrs={'class': 'panel-body'}).find_all('a')
            for link in links:
                volume.add_chapter(
                    WuxiaChapter(
                        url=self.__class__.BASE_URL+link.get('href'),
                        title=link.get_text().strip()
                    )
                )

            logging.info(f"Volume {volume} done!")


class WuxiaWorldNovelVolumeLess(WuxiaWorldNovel):
    TYPE = 'wuxiaworld_volumeless'

    def load_volumes(self):
        logging.info("Loading volumes...")

        accordion = self.index_soup.find('div', attrs={'id': 'accordion'})
        panels = accordion.find_all('div', attrs={'class': 'panel'})

        if self.skip_first:
            assert len(panels) == 2
            panel = panels[2]
        else:
            assert len(panels) == 1
            panel = panels[0]

        logging.info("Calculating total of artificial books...")

        links = panel.find('div', attrs={'class': 'panel-body'}).find_all('a')

        qt_chapter_per_book = 150
        qt_books = ceil(len(links) / qt_chapter_per_book)

        logging.info(f"Total of artificial books is {qt_books}")

        for index in range(0, qt_books):
            volume_number = index + 1
            volume = Volume()
            volume.number = str(volume_number)
            self.add_volume(volume)

            initial_index = index * qt_chapter_per_book
            final_index = initial_index + qt_chapter_per_book
            if final_index > len(links):
                final_index = len(links) - 1

            volume.title = f"book {volume.number} - {final_index - initial_index} chapters"

            for link in links[initial_index:final_index]:
                href = link.get('href')
                if href[0] == '/':
                    href = f"{self.BASE_URL}{href}"
                chapter = WuxiaChapter(url=href, title=link.get_text().strip())
                volume.add_chapter(chapter)

            logging.info(f"Volume {volume} done!")
