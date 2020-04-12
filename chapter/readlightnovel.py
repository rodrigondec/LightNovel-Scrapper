import logging

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)


class ReadLightNovelChapter(Chapter):
    def process(self):
        logging.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self.chapter_soup.find('div', attrs={'class': 'chapter-content3'})
        ps = chapter_content.find_all('p')

        ps = [p for p in ps if p.get_text().strip()]

        for p in ps:
            self.paragraphs.append(f"<p>{p.get_text()}</p>")
