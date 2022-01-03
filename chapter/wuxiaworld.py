import logging

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)


class WuxiaChapter(Chapter):
    def process(self):
        if self.pre_process():
            return

        logging.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self.chapter_soup.find('div', attrs={'id': 'chapter-content'})
        ps = chapter_content.find_all('p')

        if len(ps) <= 10:
            ps = chapter_content.find_all('div')

        ps = [p for p in ps if p.get_text().strip()]

        for p in ps:
            self.paragraphs.append(f"<p>{p.get_text()}</p>")

        self.post_process()
