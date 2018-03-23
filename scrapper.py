import requests
from bs4 import BeautifulSoup
from queue import Queue
import argparse
from time import sleep


class Scrapper():
    base_url = 'http://www.wuxiaworld.com'

    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-u', '--url', default='/novel/coiling-dragon/cd-book-6-chapter-5', help='Index of first wanted chapter')
        ap.add_argument('-qc', '--chapters', default=50, type=int, help='Quantity of chapters wanted')
        ap.add_argument('-t', '--title', default='Coiling Dragon', help='Title of the light novel')
        ap.add_argument('-d', '--delay', default=1, type=int, help=('Delay between scraping chapters (don\'t wanna '
                                                                    'get banned!)'))
        ap.add_argument('-v', '--verbose', default=True, action='store_true', help='Adds debugging statements to outpu')
        args = ap.parse_args()

        self.chapter_queue = Queue()

        self.book_title = args.title
        self.chapter_queue.put(args.url)
        self.qt_chapters = args.chapters
        self.delay = args.delay
        self.debug = args.verbose

        self.chapters = []

        self.current_soup = None

    def get_current_soup(self):
        chapter_url = self.chapter_queue.get()
        if self.debug:
            print('Geting current soup from link: {}...'.format(Scrapper.base_url + chapter_url))
        page = requests.get(Scrapper.base_url + chapter_url)

        self.current_soup = BeautifulSoup(page.content, 'html.parser')
        if self.debug:
            print('Current soup done.')
        self.get_next_link()

    def get_next_link(self):
        if self.debug:
            print('Geting link of the next chapter...')
        script = self.current_soup.find_all("script")[3]
        values = script.get_text().replace(' ', '').replace('\n', '').replace('var', '').split(';')
        next_chapter_url = None
        for value in values:
            data = value.split('=')
            if data[0] == 'NEXT_CHAPTER':
                next_chapter_url = data[1]
                next_chapter_url = next_chapter_url.replace('\'', '')
        self.chapter_queue.put(next_chapter_url)
        if self.debug:
            print('Next chapter link: {}.'.format(self.base_url + next_chapter_url))

    def proccess_soup(self):
        if self.debug:
            print('Processing current soup...')
        paragraphs = self.current_soup.find_all('p')
        chapter = {}
        chapter['title'] = paragraphs[0].get_text()
        chapter['content'] = []
        for paragraph in paragraphs[1:]:
            if paragraph.get_text() != '' and paragraph.get_text() != 'Previous Chapter' and \
                    paragraph.get_text() != 'Facebook' and paragraph.get_text() != 'Discord' and \
                    paragraph.get_text() != 'RSS' and paragraph.get_text() != 'Twitter' and \
                    paragraph.get_text() != 'Contact Us' and paragraph.get_text() != 'Privacy Policy' and \
                    paragraph.get_text() != 'Copyright © 2018 WuxiaWorld. All rights reserved.':
                chapter['content'].append(paragraph)
        if self.debug:
            print("Process of chapter {} done.".format(chapter['title']))
        self.chapters.append(chapter)

    def save_file(self):
        if self.debug:
            print("Saving chapters to html file...")
        file = open('{}.html'.format(self.book_title), 'w')
        file.write('<!doctype html><html lang="en"><head><meta charset="utf-8" />')
        file.write('<title>{}</title>'.format(self.book_title))
        file.write('<style>p { margin-top: 1em; text-indent: 0em; } h1 {margin-top: 1em; text-align: center} h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;} h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;} .center { text-align: center; } .pagebreak { page-break-before: always; }</style>')
        file.write('</head><body>')
        file.write('<h1>{}</h1><div class="pagebreak"></div>'.format(self.book_title))
        file.write('<div id="toc">'
                   '<h2>'
                   'Table of Contents <br />'
                   '</h2>'
                   '<ul>')

        for index in range(0, len(self.chapters)):
            file.write('<li><a href="#ch{index}">{title}</a></li>'.format(index=index+1, title=self.chapters[index]['title']))
        file.write('</ul></div><div class="pagebreak"></div>')

        index = 0
        for chapter in self.chapters:
            file.write('<h3 id="ch{}">'.format(index+1))
            file.write(chapter['title'])
            file.write('</h3>')
            index += 1
            for paragraph in chapter['content']:
                file.write('<p>')
                file.write(paragraph.get_text())
                file.write('</p>')
            file.write('<div class="pagebreak"></div>')
        file.write('</body>'
                   '</html>')
        file.close()
        if self.debug:
            print('File html saved.')

    def start(self):
        if self.debug:
            print('Scrapper initializing...')
        for x in range(0, self.qt_chapters):
            self.get_current_soup()
            self.proccess_soup()
            sleep(self.delay)
        self.save_file()

if __name__ == '__main__':
    Scrapper().start()