# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests,json


class MyfilmfinderPipeline(object):
    def process_item(self, item, spider):
        it=str(item)
        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        requests.post('http://127.0.0.1:5000/post/', data=json.dumps(it), headers=headers)
        return item