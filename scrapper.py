import requests
from bs4 import BeautifulSoup
from queue import Queue

qt_chapters = 50
base_url = 'http://www.wuxiaworld.com'
chapter_queue = Queue()
chapter_queue.put('/novel/coiling-dragon/cd-book-6-chapter-5')
book_title = 'Coiling Dragon'

chapters = []

for x in range(0, qt_chapters):
    chapter_url = chapter_queue.get()
    print("URL: " + base_url + chapter_url)
    page = requests.get(base_url + chapter_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # print(soup)

    script = soup.find_all("script")[3]
    values = script.get_text().replace(' ', '').replace('\n', '').replace('var', '').split(';')
    next_chapter_url = None
    for value in values:
        data = value.split('=')
        if data[0] == 'NEXT_CHAPTER':
            next_chapter_url = data[1]
            next_chapter_url = next_chapter_url.replace('\'', '')
            print("next url: " + next_chapter_url)
    chapter_queue.put(next_chapter_url)

    paragraphs = soup.find_all('p')
    chapter = []
    for paragraph in paragraphs:
        if paragraph.get_text() != '' and paragraph.get_text() != 'Previous Chapter' and \
                paragraph.get_text() != 'Facebook' and paragraph.get_text() != 'Discord' and \
                paragraph.get_text() != 'RSS' and paragraph.get_text() != 'Twitter' and \
                paragraph.get_text() != 'Contact Us' and paragraph.get_text() != 'Privacy Policy' and \
                paragraph.get_text() != 'Copyright © 2018 WuxiaWorld. All rights reserved.':
            chapter.append(paragraph)
    print("Chapter done.")
    chapters.append(chapter)
print(chapters)

book = open(book_title+'.html', 'w')
book.write('<!doctype html><html lang="en"><head><meta charset="utf-8" />'
           '<title>'+book_title+'</title>'
           '<style>p { margin-top: 1em; text-indent: 0em; } h1 {margin-top: 1em; text-align: center} h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;} h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;} .center { text-align: center; } .pagebreak { page-break-before: always; }</style></head><body>')
book.write('<h1>'+book_title+'</h1><div class="pagebreak"></div>')
book.write('<div id="toc">'
           '<h2>'
           'Table of Contents <br />'
           '</h2>'
           '<ul>')

for index in range(0, len(chapters)):
    book.write('<li><a href="#ch'+str(index+1)+'">'+chapters[index][0].get_text()+'</a></li>')
book.write('</ul></div><div class="pagebreak"></div>')

index = 0
for chapter in chapters:
    book.write('<h3 id="ch'+str(index)+'">')
    book.write(chapter[0].get_text())
    book.write('</h3>')
    index += 1
    for paragraph in chapter[1:]:
        book.write('<p>')
        book.write(paragraph.get_text())
        book.write('</p>')
    book.write('<div class="pagebreak"></div>')
book.write('</body>'
           '</html>')
book.close()
