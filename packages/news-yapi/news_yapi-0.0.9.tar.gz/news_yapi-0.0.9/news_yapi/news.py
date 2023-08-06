from newsapi import NewsApiClient
from appPublic.timeUtils import curDateString
from uninews.baseprovider import BaseProvider
from .version import __version__

app_info = {}

def set_app_info(appkey):
	app_info.update({
		'appkey':appkey
	})

def buildProvider(newsfeed):
	print(f'news_yapi version {__version__}')
	return NewsApi(newsfeed)

class NewsApi(BaseProvider):
	def __init__(self, newsfeed):
		self.newsfeed = newsfeed
		self.api = NewsApiClient(api_key=app_info.get('appkey'))

	def get_result_mapping(self):
		return {
			'total':'totalResults',
			'articles':'articles'
		}
	
	def get_article_mapping(self):
		return {
			'link':'url',
			'img_link':'urlToImage',
			'publish_date':'publishedAt'
		}
	
	def sources_result_mapping(self):
		return {}

	def source_mapping(self):
		return {
			'link':'url',
			'categories':'category',
			'countries':'country'
		}

	def sources(self, countries=[], categories=[], language=[]):
		categories = None if len(categories) == 0 else categories[0]
		language_str = None if len(language) == 0 else language[0]
		countries_str = None if len(countries) == 0 else countries[0]
		return self.api.get_sources(country=countries_str,
						category=categories,
						language=language_str
		)

	def last_news(self, q=None, 
						domains=[],
						sources=[],
						categories=[],
						countries=[], 
						language=[], 
						page=0):
		keyword = q
		if keyword == '':
			keyword = None
		categories = None if len(categories) == 0 else categories[0]
		language_str = None if len(language) == 0 else language[0]
		countries_str = None if len(countries) == 0 else countries[0]
		sources = self.newsfeed.array2param(sources)
		return self.api.get_top_headlines(q=keyword,
							country=countries_str,
							category=categories,
							sources=sources,
							language=language_str,
							page=page)

	def hist_news(self, q=None, categories=[],
						countries=[], 
						language=[], 
						domains=[],
						sources=[],
						from_date=None,
						to_date=None,
						page=0):
		keyword = q
		if keyword == '':
			keyword = None
		categories = None if len(categories) == 0 else categories[0]
		language_str = None if len(language) == 0 else language[0]
		countries_str = None if len(countries) == 0 else countries[0]
		sources = self.newsfeed.array2param(sources)
		domains = self.newsfeed.array2param(domains)
		return self.api.get_everything(q=keyword,
							sources=sources,
							domains=domains,
							from_param=from_date,
							to=to_date,
							page=page)


if __name__ == '__main__':
	print('input appkey:')
	appkey=input()
	set_app_info(appkey)
	nc = NewsApi()
	while True:
		print('key word to search news, ":quit" to exit')
		x = input()
		if x == ':quit':
			break
		news = nc.getNews(x)
		print(news.keys())
		print(news['results'][0].keys())
