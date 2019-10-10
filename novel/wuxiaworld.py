import logging
from math import ceil

from novel.base import Novel
from volume.base import Volume
from chapter.wuxiaworld import WuxiaChapter

logging.basicConfig(level=logging.INFO)


class WuxiaWorldNovel(Novel):

    BASE_URL = 'http://www.wuxiaworld.com'

    @classmethod
    def from_data(cls, data):
        return cls(data.get('title'), data.get('index_url'), data.get('skip_first'))

    def __init__(self, title, index_url, skip_first):
        self.skip_first = skip_first

        super(WuxiaWorldNovel, self).__init__(title, index_url)

    def __str__(self):
        return f"Novel {self.title}"

    def load_volumes(self):
        logging.info("Loading volumes...")

        accordion = self.index_soup.find('div', attrs={'id': 'accordion'})
        panels = accordion.find_all('div', attrs={'class': 'panel'})

        for panel in panels:
            volume = Volume()
            volume.number = int(panel.find('h4').find('span', attrs={'class': 'book'}).get_text())

            if self.skip_first:
                volume.number -= 1
                if volume.number == 0:
                    continue

            volume.number = str(volume.number)
            if not self._is_volume_chosen(volume.number):
                continue

            volume.title = panel.find('h4').find('span', attrs={'class': 'title'}).find('a').get_text().strip()

            links = panel.find('div', attrs={'class': 'panel-body'}).find_all('a')
            for link in links:
                volume.add_chapter(
                    WuxiaChapter(
                        url=self.__class__.BASE_URL+link.get('href'),
                        title=link.get_text().strip()
                    )
                )

            self.volumes.append(volume)
            logging.info(f"Volume {volume} done!")


class WuxiaWorldNovelVolumeLess(WuxiaWorldNovel):
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
            volume.number = volume_number

            volume.number = str(volume.number)

            if not self._is_volume_chosen(volume.number):
                continue

            initial_index = index * qt_chapter_per_book
            final_index = initial_index + qt_chapter_per_book
            if final_index > len(links):
                final_index = len(links) - 1

            volume.title = f"book {volume.number} - {final_index - initial_index} chapters"

            for link in links[initial_index:final_index]:
                volume.add_chapter(WuxiaChapter(url=link.get('href'), title=link.get_text().strip()))

            self.volumes.append(volume)
            logging.info(f"Volume {volume} done!")
