# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem

class LianjiaCJPipeline(object):

    def process_item(self, item, spider):
        print (spider.name=='ljcj')
        if item['totalPrice'] < 10:
            raise DropItem("totalPrice too small %s" % item)
        
        if item['title']:
            xiaoqu, huxin, square = item['title'].split(' ')
            return item
        else:
            raise DropItem("Missing title in %s" % item)
        
class LianjiaZSPipeline(object):

    def process_item(self, item, spider):
        print (spider.name=='ljzs')
        if int(item['totalPrice']) < 10:
            raise DropItem("totalPrice too small %s" % item)
        
        if item['title']:
            xiaoqu, huxin, square = item['title'].split(' ')
            return item
        else:
            raise DropItem("Missing title in %s" % item)      