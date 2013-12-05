from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from myfilmfinder.items import MyFilmItem
from scrapy.selector import Selector
import re

class NowTV(CrawlSpider):
	count = 0
	name = "nowtvspider"
	start_urls = ['http://watch.nowtv.com/movies/genres',]
	allowed_domains = ['watch.nowtv.com',]
	rules = (
			Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="ng-app"]/body/div[3]/div/section/section/section/h2/a')),follow=True),
			Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="genreList"]')),callback='parse_movie'),
			)

	def parse_movie(self, response):
		self.count += 1
		sel = Selector(response)

		MOVIEID_XPATH = sel.xpath('//*[@id="ng-app"]//article/div[3]/@stream-id').extract()
		TITLE_XPATH = sel.xpath('//*[@id="ng-app"]//article/h1/text()').extract()
		YEAR_XPATH = sel.xpath('//*[@id="ng-app"]//article/ul/li[1]/span/text()').extract()
		DURATION_XPATH = sel.xpath('//*[@id="ng-app"]//article/ul/li[2]/span/text()').extract()
		RATING_XPATH = sel.xpath('//*[@id="ng-app"]//article/ul/li[3]/span/text()').extract()
		BUYPRICE_XPATH = 'N/A'
		PRICE_XPATH = 'N/A'
		url = response.url
		providerid = '4'
		movieid = MOVIEID_XPATH[0] if MOVIEID_XPATH else 'N/A'
		title = TITLE_XPATH[0] if TITLE_XPATH else 'N/A'
		year = YEAR_XPATH[0] if YEAR_XPATH else 'N/A'
		duration = DURATION_XPATH[0] if DURATION_XPATH else 'N/A'
		rating = RATING_XPATH[0] if RATING_XPATH else 'N/A'
		buyprice = BUYPRICE_XPATH
		price = PRICE_XPATH

		item = MyFilmItem(
			url=url,
			movieid=movieid,
			title=title,
			year=year,
			duration=duration,
			rating=rating,
			buyprice=buyprice,
			price=price,
			providerid=providerid,
            pid='1',
			)
		yield item