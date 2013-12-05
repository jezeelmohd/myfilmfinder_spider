# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MyFilmItem(Item):
    url = Field()
    movieid = Field()
    title = Field()
    rating = Field()
    year = Field()
    duration = Field()
    price = Field()
    buyprice = Field()
    pid = Field()
    providerid = Field()
