# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
import re
from myfilmfinder.items import MyFilmItem
import requests

class NetFlix(BaseSpider):
	name = 'netflixspider'
	start_urls = ['https://signup.netflix.com/globallogin',]
	#start_urls = ['http://proxymesh.com/web/browse.php?u=eqD2cjJDEtMJnJ%2FSZuSqnfI1Myo2E6liMYuNo5K0UDZTxQ%3D%3D',]
	#start_urls = ['http://www.justproxy.co.uk/index.php?q=aHR0cHM6Ly9zaWdudXAubmV0ZmxpeC5jb20vZ2xvYmFsbG9naW4%3D&hl=2ed',]
	def parse(self, response):
		EMAIL = "jamie.derrick@gmail.com"
		PASS = '0xf0rd£9.99'
		req = [FormRequest.from_response(response,formdata={'email':EMAIL, 'password':PASS},callback=self.after_login)]
		return req
	def after_login(self, response):
		return Request("http://movies.netflix.com/WiHome",dont_filter=True,
					callback=self.parse_genre)
	def parse_genre(self, response):
		#inspect_response(response)
		sel = Selector(response)
		genres = sel.xpath('//*[@id="bd"]/div/div/div[1]/h3/a/@href').extract()
		if genres:
			for gen in genres[7:]:
				yield Request(url=gen,callback=self.parse_movielist)

	def parse_movielist(self, response):
		sel = Selector(response)
		movies = sel.xpath('//*[@id="yui-main"]/div/div[1]/div[2]/div/div')
		if movies:
			for mov in movies:
				alt = mov.xpath('span/img/@alt').extract()
				alt_clean = alt[0].replace(':','').replace(" ","_") if alt else None
				mid = mov.xpath('span/a/@id').extract()
				mid_clean = mid[0].replace('b0','').replace('_0','') if mid else None
				if alt_clean and mid_clean:
					#movie_url = 'http://movies.netflix.com/WiMovie/'+alt_clean+'/'+mid_clean+'?locale=enGB'
					movie_url = 'http://movies.netflix.com/WiMovie/'+alt_clean+'/'+mid_clean
					yield Request(url=movie_url, callback=self.parse_movie)

	def parse_movie(self, response):
		r=requests.get(response.url)
		sel = Selector(text=r.content)
		#sel = Selector(response)
		TITLE_XPATH = sel.xpath('//*[@id="displaypage-overview-details"]/div[1]/div/h1/text()').extract()
		YEAR_XPATH = sel.xpath('//*[@id="displaypage-overview-details"]/div[1]/span[1]/text()').extract()
		RATING_XPATH = sel.xpath('//*[@id="displaypage-overview-details"]/div[1]/span[2]/@class').extract()
		RATING_XPATH_TEXT = sel.xpath('//*[@id="displaypage-overview-details"]/div[1]/span[2]/text()').extract()
		DURATION_XPATH = sel.xpath('//*[@id="displaypage-overview-details"]/div[1]/span[@class="duration"]/text()').extract()
		PROG_TYPE_XPATH = sel.xpath('//*[@id="displaypage-details"]/div/h3[1]/text()').extract()
		BUYPRICE_XPATH = 'N/A'
		PRICE_XPATH = 'N/A'

		url = response.url
		movieid = url.split('/')[-1].replace('?locale=enGB','')
		title = TITLE_XPATH[0] if TITLE_XPATH else 'N/A'
		year = YEAR_XPATH[0] if YEAR_XPATH else 'N/A'
		if RATING_XPATH_TEXT:
			if 'certRating' in RATING_XPATH[0]:
				rating = RATING_XPATH_TEXT[0] if RATING_XPATH_TEXT else 'N/A'
			else:
				rating = 'N/A'
		elif RATING_XPATH:
			rating = ' '.join(RATING_XPATH).split()[-1] if RATING_XPATH else 'N/A'
		else:
			rating = 'N/A'
		if 'certRating' in rating:
			rating = 'N/A'
		duration = DURATION_XPATH[0] if DURATION_XPATH else 'N/A'
		if 'Season' in duration:
			duration = 'N/A'
		elif 'Episode' in duration:
			duration = 'N/A'
		elif 'Collection' in duration:
			duration = 'N/A'
		elif 'Series' in duration:
			duration = 'N/A'
		elif 'Part' in duration:
			duration = 'N/A'
		prog_type = PROG_TYPE_XPATH[0] if PROG_TYPE_XPATH else 'N/A'
		if 'Movie' in prog_type:
			pid = 1
		elif 'Film' in prog_type:
			pid = 1
		elif 'Programme' in prog_type:
			pid = 2
		elif  'Show' in prog_type:
			pid = 2
		else:
			pid = 'notavail'
		buyprice = BUYPRICE_XPATH
		price = PRICE_XPATH

		item = MyFilmItem(
			movieid=movieid,
			title=title,
			year=year,
			duration=duration,
			rating=rating,
			buyprice=buyprice,
			price=price,
			pid=pid,
			url=url,
			providerid = '2',
			)
		if pid!='notavail':
			yield item
