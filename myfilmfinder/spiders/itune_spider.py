from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.http import Request
from myfilmfinder.items import MyFilmItem
import re


class ItuneSpider(CrawlSpider):
	count = 0
	name = 'itunesspider'
	start_urls = ['https://itunes.apple.com/gb/genre/films/id33',]
	rules = (
			Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="genre-nav"]')),follow=True,),
			Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="selectedgenre"]/ul[1]')),follow=True,),
			Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="selectedgenre"]/ul[2]')),follow=True,),
			Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="selectedcontent"]')),callback='parse_movie')
			)

	def parse_movie(self,response):
		sel = Selector(response)
		self.count += 1
		TITLE_XPATH = sel.xpath('//*[@id="title"]/div[1]/h1/text()').extract()
		MOVIE_URL_XPATH = sel.xpath('/html/head/link[1]/@href').extract()[0]
		YEAR_XPATH = sel.xpath('//*[@id="left-stack"]/div[1]/ul/li[3]/text()').extract()
		RATING_XPATH = sel.xpath('//*[@id="title"]/div[1]/span/text()').extract()
		BUY_PRICE_XPATH = sel.xpath('//*[@id="left-stack"]/div[1]/ul/li[1]/span/text()').extract()

		if TITLE_XPATH:
			title = TITLE_XPATH[0]
		else:
			title =  "N/A"
		if MOVIE_URL_XPATH:
			MOVIE_SPLIT = MOVIE_URL_XPATH.split("/")
			movieid = MOVIE_SPLIT[-1].replace('id','')
		else:
			movieid = "N/A"
		if RATING_XPATH:
			rating = RATING_XPATH[0]
		else:
			rating = "N/A"
		if YEAR_XPATH:
			year = YEAR_XPATH[0]
		else:
			year = "N/A"
		duration = "N/A"
		url = MOVIE_URL_XPATH
		if BUY_PRICE_XPATH:
			buyprice = re.compile('\d+.\d+').findall(BUY_PRICE_XPATH[0])[0]
		else:
			buyprice='N/A'
		price = "N/A"
		pid = 1
		item = MyFilmItem(
			title=title,
			movieid=movieid,
			rating=rating,
			year=year,
			url=url,
			buyprice=buyprice,
			price=price,
			pid=pid,
			providerid='5',
			duration=duration,
			)
		yield item