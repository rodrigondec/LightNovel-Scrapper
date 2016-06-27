from lxml import html
import requests



capitulos = input("num de capitulos: ")

url = raw_input('url do cap 1: ')
# url = 'http://www.wuxiaworld.com/st-index/st-book-1-chapter-1/'

file = open('livro.html', 'w')

file.write('<body style="width: 50%;float: none; margin: auto; background-color: #121110;">')

for x in xrange(0, capitulos):
	print "cap "+str(x+1)
	file.write('<h2><font color="#7C7567">')
	file.write(url)
	file.write('</font></h2>')

	page = requests.get(url)
	tree = html.fromstring(page.content)

	paragrafos = tree.xpath('//div[@itemprop="articleBody"]/p/text()')
	paragrafos = paragrafos[1:len(paragrafos)-3]
	for paragrafo in paragrafos:
		# print>>file, paragrafo.encode('utf-8')
		file.write('<p><font size="5" color="#7C7567">')
		file.write(paragrafo.encode('utf-8'))
		file.write('</font></p>')
		# print paragrafo


	# file.write("\n\n")

	url = tree.xpath('//div[@itemprop="articleBody"]/p/span[@style="float: right;"]/a/@href')
	url  = url[0]
	# print url

file.write('</body>')

file.close()