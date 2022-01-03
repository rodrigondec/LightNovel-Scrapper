import logging

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)


class WuxiaChapter(Chapter):
    def process(self):
        if self._loaded_from_cache:
            return

        logging.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self._soup.find('div', attrs={'id': 'chapter-content'})
        ps = chapter_content.find_all('p')

        if len(ps) <= 10:
            ps = chapter_content.find_all('div')

        ps = [p for p in ps if p.get_text().strip()]

        for p in ps:
            self._paragraphs.append(f"<p>{p.get_text()}</p>")

        self._save_cache()
