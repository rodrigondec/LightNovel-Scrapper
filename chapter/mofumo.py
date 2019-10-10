import logging

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)


class MofumoChapter(Chapter):
    def process(self):
        logging.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self.chapter_soup.find('div', attrs={'class': 'entry-content'})
        ps = chapter_content.find_all('p')

        for p in ps:
            if p.get_text():
                self.paragraphs.append(f"<p>{p.get_text()}</p>")
