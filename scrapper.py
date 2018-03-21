import requests
from bs4 import BeautifulSoup
from queue import Queue


qt_chapters = 50
base_url = 'http://www.wuxiaworld.com'
chapter_queue = Queue()
chapter_queue.put('/novel/coiling-dragon/cd-book-1-chapter-1')

chapters = []

for x in range(0, qt_chapters):
    chapter_url = chapter_queue.get()
    print("URL: "+base_url+chapter_url)
    page = requests.get(base_url+chapter_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # print(soup)

    script  = soup.find_all("script")[3]
    values = script.get_text().replace(' ', '').replace('\n', '').replace('var', '').split(';')
    next_chapter_url = None
    for value in values:
        data = value.split('=')
        if data[0] == 'NEXT_CHAPTER':
            next_chapter_url = data[1]
            next_chapter_url = next_chapter_url.replace('\'', '')
            print("next url: "+next_chapter_url)
    chapter_queue.put(next_chapter_url)

    paragraphs = soup.find_all('p')
    chapter = []
    for paragraph in paragraphs :
        if paragraph.get_text() != '' and paragraph.get_text() != 'Previous Chapter' and \
            paragraph.get_text() != 'Facebook' and paragraph.get_text() != 'Discord' and \
            paragraph.get_text() != 'RSS' and paragraph.get_text() != 'Twitter' and \
            paragraph.get_text() != 'Contact Us' and paragraph.get_text() != 'Privacy Policy' and \
            paragraph.get_text() != 'Copyright © 2018 WuxiaWorld. All rights reserved.':
            chapter.append(paragraph)
    print("Chapter done.")
    chapters.append(chapter)
print(chapters)

book = open('book.html', 'w')
for chapter in chapters:
    for paragraph in chapter:
        book.write(str(paragraph))

book.close()
