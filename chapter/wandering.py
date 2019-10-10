import logging

import bs4

from chapter.base import Chapter


logging.basicConfig(level=logging.INFO)


class WanderingChapter(Chapter):
    def process(self):
        logging.info(f"Processing paragraphs for chapter {self}...")
        self.load_soup()

        chapter_content = self.chapter_soup.find('div', attrs={'class': 'entry-content'})
        assert isinstance(chapter_content, bs4.Tag)
        elements = chapter_content.find_all()
        for i in range(0, len(elements)):
            if elements[i].name == 'hr':
                elements = elements[i+1:]
                break

        for element in elements:
            if element.get_text().strip():
                self.paragraphs.append(f"<p>{element.get_text()}</p>")
