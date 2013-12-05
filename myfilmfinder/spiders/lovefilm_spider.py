from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
from myfilmfinder.items import MyFilmItem
import re


class LoveFIlm(CrawlSpider):
    count = 0
    name = 'lovefilmspider'
    start_urls = [
        'http://www.lovefilm.com/c/?token=%253Fu%253D%25252Fcatalog%25252Fvideo%25253Funique%25253Dseries%252526sort%25253Ddemand%25252Bdesc%252526mature%25253D0%252526expand%25253Dnone%252526action%25253Dall%252526type%25253Dseries%25252BOR%25252Bfeature%25252BOR%25252Bfilm%25252BOR%25252Bgame%252526items_per_page%25253D10%252526f%25253D_fmt%2525257Cdigital%252526adult%25253D0%252526start_index%25253D1%2526m%253DGET&sort=demand+desc']
    allowed_domains = ['lovefilm.com', ]
    rules = (
        Rule(SgmlLinkExtractor(
            restrict_xpaths='//*[@id="main-content"]/div[2]/div[2]/ul'), follow=True),
        Rule(
            SgmlLinkExtractor(
                restrict_xpaths=(
                    '//*[@id="main-content"]/div[2]/div[3]',
                    '//*[@id="main-content"]/div[2]/div[4]',), allow=('.+\/film\/.+', '.+\/tv\/.+')), callback='parse_movie')
    )

    def parse_movie(self, response):
        self.count += 1
        sel = Selector(response)
        URL_XPATH = sel.xpath('/html/head/link[2]/@href').extract()
        TITLE_XPATH = sel.xpath(
            '//*[@id="product-summary"]/h1/span/text()').extract()
        YEAR_XPATH = sel.xpath(
            '//*[@id="product-summary"]/span[@class="title-details"]/text()').extract()
        DURATION_XPATH = sel.xpath(
            '//*[@id="fro_content"]/div[1]/table[2]/tr[1]/td/text()').extract()
        url = URL_XPATH[0]
        MOVIE_SPLIT_URL = url.split("/")
        movieid = MOVIE_SPLIT_URL[-2]
        pid = MOVIE_SPLIT_URL[3]
        if pid == "film":
            pid = 1
            RATING_XPATH = sel.xpath(
                '//*[@class="zebra"]/tr[2]/td[3]/span/text()').extract()
        elif pid == "tv":
            pid = 2
            if YEAR_XPATH:
                RATING_XPATH = sel.xpath(
                    '//*[@id="product-summary"]/span[2]/text()').extract()
            else:
                RATING_XPATH = sel.xpath(
                    '//*[@id="product-summary"]/span/text()').extract()

        if TITLE_XPATH:
            title = TITLE_XPATH[0]
        else:
            title = "N/A"
        if YEAR_XPATH:
            year = YEAR_XPATH[0]
        else:
            year = "N/A"
        if RATING_XPATH:
            rating = RATING_XPATH[0]
        else:
            rating = "N/A"
        if DURATION_XPATH:
            duration = DURATION_XPATH[0]
        else:
            duration = "N/A"
        item = MyFilmItem(
            url=url,
            movieid=movieid,
            pid=pid,
            title=title,
            year=year,
            rating=rating,
            duration=duration,
            providerid=1,
            price='N/A',
            buyprice='N/A',
        )
        yield item
