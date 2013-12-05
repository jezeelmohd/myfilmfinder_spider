from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from myfilmfinder.items import MyFilmItem
import re

class BinkBox(CrawlSpider):
	name = 'blinkboxspider'
	start_urls = ['http://www.blinkbox.com/movies','http://www.blinkbox.com/tv']
	#start_urls = ['http://4.hidemyass.com/ip-1/encoded/Oi8vd3d3LmJsaW5rYm94LmNvbS9tb3ZpZXM%3D&f=norefer','http://4.hidemyass.com/ip-1/encoded/Oi8vd3d3LmJsaW5rYm94LmNvbS90dg%3D%3D&f=norefer']
	#allowed_domains = ['blinkbox.com',]
	rules = (
			Rule(SgmlLinkExtractor(restrict_xpaths=('/html/body/main/div/div[1]/ul/li/article/h1/a')),callback='parse_movie'),
			Rule(SgmlLinkExtractor(restrict_xpaths=('/html/body/main/div/div[1]//a[@class="nextPage"]')),follow=True),
			)

	def parse_movie(self, response):
		sel = Selector(response)
		META_URL = sel.xpath('//meta[@property="og:url"]/@content').extract()
		DETAILS_LIST_XPATH = sel.xpath('//*[@class="headerInnerWrapper"]/ul/li/text()').extract()

		TITLE_XPATH = sel.xpath('//*[@class="headerInnerWrapper"]/h1/text()').extract()
		RENT_PRICE_XPATH =  sel.xpath('//*[@class="orangeButton"]/p/text()').extract()
		META_URL = META_URL[0]
		M_ID = META_URL.split('/')[4]
		movieid = re.compile('\d+').findall(M_ID)[-1]
		pid = META_URL.split('/')[3]
		if pid=="movies":
			pid = 1
			BUY_PRICE_XPATH = sel.xpath('//*[@class="blueButton"]/p/text()').extract()
		elif pid=="tv":
			pid = 2
			BUY_PRICE_XPATH = sel.xpath('//*[@class="price"]/text()').extract()
		rating=''
		year=''
		duration=''
		if DETAILS_LIST_XPATH:
			for detail in DETAILS_LIST_XPATH:
				if re.compile('CERT\s\w+').findall(detail):
					rating = detail.strip('CERT')
				elif re.compile('\d{4}').findall(detail):
					year = detail
				elif ('HR' in detail or 'MIN' in detail):
					duration = detail

				else:
					if rating=="":
						rating = "N/A"
					if year=="":
						year = "N/A"
					if duration=="":
						duration = "N/A"
		if TITLE_XPATH:
			title = TITLE_XPATH[0]
		else:
			title = "N/A"
		if RENT_PRICE_XPATH:
			price = re.compile('\d+.\d+').findall(RENT_PRICE_XPATH[0])
			if price:
				price = price[0]
			else:
				price = "N/A"
		else:
			price = "N/A"

		if BUY_PRICE_XPATH:
			buyprice = re.compile('\d+.\d+').findall(BUY_PRICE_XPATH[0])
			if buyprice:
				buyprice = buyprice[0]
			else:
				buyprice = "N/A"
		else:
			buyprice = "N/A"
		item = MyFilmItem(
			url = META_URL,
			movieid = movieid,
			title = title,
			rating = rating,
			year = year,
			duration = duration,
			price = price,
			buyprice = buyprice,
			pid = pid,
			providerid = '3',
			)
		yield item