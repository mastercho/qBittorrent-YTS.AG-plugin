#VERSION: 1.0
#AUTHOR: Aydan Aleydin (ameldur1337@gmail.com)
#LICENSE: Gnu General Public License v2 or later

from novaprinter import prettyPrinter
from bs4 import BeautifulSoup
from helpers import retrieve_url, download_file

LINK = 9
NAME = 1
RATING = 5
SIZE = 2
SEEDS = 8
SEEN_ITEMS = []

class yts(object):
	url = 'http://yts.ag'
	name = 'YTS'
	
	def __init__(self):
		self.results = []

	def download_torrent(self, info):
		print download_file(info)

	def parse(self, soup):
		item_count = 0
		for info in soup('div', 'browse-info'):
			spans = info('span')
			item = {}
			item['link'] = spans[LINK]('a')[1].get('href')

			if item['link'] in SEEN_ITEMS:
				continue
			else:
				SEEN_ITEMS.append(item['link'])

			rating = spans[RATING].get_text().replace('IMDB Rating: ', '')
			rating = rating.replace('/10', '')
			item['name'] = spans[NAME].get_text() + ' [' + rating + ']'
			item['size'] = spans[SIZE].get_text().replace('Size: ', '')
			item['seeds'] = spans[SEEDS].get_text().replace('Seeds: ', '')
			item['leech'] = "-1"
			item['engine_url'] = self.url

			
			prettyPrinter(item)
			item_count += 1
		return item_count

	def search(self, what, cat='all'):
		page = 1

		if cat not in ['all', 'movies']:
			return

		while page <= 10:
			url = self.url+'/browse-movie/%s/All/All/0/seeds/%d' % (what, page)
			soup = BeautifulSoup(retrieve_url(url))
			results = self.parse(soup)
			if results <= 0:
				break
			page += 1
