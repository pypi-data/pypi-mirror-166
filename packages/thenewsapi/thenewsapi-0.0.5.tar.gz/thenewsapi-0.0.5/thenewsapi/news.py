import requests
from appPublic.http_client import Http_Client
from appPublic.timeUtils import curDateString
from uninews.baseprovider import BaseProvider
from .version import __version__
app_info = {}

def set_app_info(appkey):
	app_info.update({
		'appkey':appkey
	})

def buildProvider(newsfeed):
	print(f'TheNewsApi version {__version__}')
	return TheNewsApi(newsfeed)

class TheNewsApi(BaseProvider):
	def __init__(self, newsfeed):
		self.newsfeed = newsfeed
		self.appkey = app_info.get('appkey')

	def get_result_mapping(self):
		return {
			'total':'meta.found',
			'rows':'meta.limit',
			'page':'meta.page',
			'articles':'data'
		}
	
	def get_article_mapping(self):
		return {
			'link':'url',
			'img_link':'image_url',
			'publish_date':'published_at'
		}
	
	def sources_result_mapping(self):
		return {
			'total':'meta.found',
			'sources':'data'
		}

	def source_mapping(self):
		return {
			'id':'source_id',
			'name':'domain',
			'countries':'locale'
		}

	def last_news(self, q=None, 
						categories=[],
						countries=[], 
						domains=[],
						sources=[],
						language=[], 
						page=0):
		url = 'https://api.thenewsapi.com/v1/news/all'
		keyword = q
		if keyword == '':
			keyword = None
		categories = self.newsfeed.array2param(categories)
		language_str = self.newsfeed.array2param(language)
		countries_str = self.newsfeed.array2param(countries)
		domains = self.newsfeed.array2param(domains)
		sources = self.newsfeed.array2param(sources)
		p = {
			'api_token':self.appkey,
			'categories':categories, 
			'language':language_str,
			'published_on':curDateString(),
			'domains':domains,
			'source_ids':sources,
			'locale':countries,
			'page':page,
			'search':keyword
		}
		# print(url, p)
		hc = Http_Client()
		x = hc.get(url, params=p)
		return x

	def hist_news(self, q=None, categories=[],
						countries=[], language=[], 
						sources=[],
						domains=[],
						from_date=None,
						to_date=None,
						page=0):
		url = 'https://api.thenewsapi.com/v1/news/top'
		keyword = q
		if keyword == '':
			keyword = None
		categories = self.newsfeed.array2param(categories)
		language_str = self.newsfeed.array2param(language)
		countries_str = self.newsfeed.array2param(countries)
		domains = self.newsfeed.array2param(domains)
		sources = self.newsfeed.array2param(sources)
		p = {
			'api_token':self.appkey,
			'categories':categories, 
			'language':language_str,
			'published_on':curDateString(),
			'domains':domains,
			'sources':sources,
			'published_after':from_date,
			'published_before':to_date,
			'page':page,
			'search':keyword
		}
		# print(url, p)
		hc = Http_Client()
		x = hc.get(url, params=p)
		return x

	def sources(self, categories=[], language=[], countries=[]):
		categories = self.newsfeed.array2param(categories)
		language_str = self.newsfeed.array2param(language)
		countries_str = self.newsfeed.array2param(countries)
		url = 'https://api.thenewsapi.com/v1/news/sources'
		p = {
			'api_token':self.appkey,
			'categories':categories,
			'language':language_str
		}
		hc = Http_Client()
		x = hc.get(url, params=p)
		return x

if __name__ == '__main__':
	print('input appkey:')
	appkey=input()
	set_app_info(appkey)
	nc = TheNewsApi()
	while True:
		print('key word to search news, ":quit" to exit')
		x = input()
		if x == ':quit':
			break
		news = nc.getNews(x)
		print(news.keys())
		print(news['results'][0].keys())
