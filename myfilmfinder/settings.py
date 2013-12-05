# Scrapy settings for myfilmfinder project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'myfilmfinder'

SPIDER_MODULES = ['myfilmfinder.spiders']
NEWSPIDER_MODULE = 'myfilmfinder.spiders'
#ITEM_PIPELINES = ['myfilmfinder.pipelines.MyfilmfinderPipeline',]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myfilmfinder (+http://www.yourdomain.com)'
"""
SENTRY_DSN = 'http://0a6c1fd3393d49f8bca16ea413dc4fc9:43a1a216efe34a0e87cffd4993fc64ba@146.185.172.237:9000/2'
EXTENSIONS = {
  "scrapy_sentry.extensions.Errors":10,
}
"""
DOWNLOADER_MIDDLEWARES = {
}

"""
'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
'myfilmfinder.middleware.ProxyMiddleware': 100,
'myfilmfinder.middleware.RandomUserAgentMiddleware': 400,
'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
"""