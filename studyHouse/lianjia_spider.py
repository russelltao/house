#coding=utf-8
import scrapy
from .items import LianjiaCJItem,LianjiaZSItem
import json

ljurl = 'https://hz.lianjia.com'
hzarea2 = ['binjiang','xihu','xiacheng','jianggan','gongshu','shangcheng','yuhang','xiaoshan']
hzarea = ['binjiang']

hzurlzs,hzurlcj = [],[]
for area in hzarea:
    hzurlzs.append('%s/ershoufang/%s'%(ljurl, area))

class LianjiaZSSpider(scrapy.Spider):
    name = "ljzs"
    allowed_domains = ["lianjia.com"]
    start_urls = hzurlzs
    
    def parseOneItem(self, sel, area, subarea):
        item = LianjiaZSItem()
        item['area'] = area
        item['subarea'] = subarea
        item['totalPrice'] = sel.xpath('div[@class="address"]/div[@class="totalPrice"]/span/text()').extract_first()

        item['title'] = sel.xpath('div[@class="title"]/a/text()').extract_first()
        item['dealDate'] = sel.xpath('div[@class="address"]/div[@class="dealDate"]/text()').extract_first()
        
        item['houseInfo'] = sel.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').extract_first()
        
        item['positionInfo']= sel.xpath('div[@class="flood"]/div[@class="positionInfo"]/text()').extract_first()
        item['source']= sel.xpath('div[@class="flood"]/div[@class="source"]/text()').extract_first()
        item['unitPrice']= sel.xpath('div[@class="flood"]/div[@class="unitPrice"]/span/text()').extract_first()
        item['followInfo']= sel.xpath('div[@class="followInfo"]/div[@class="starIcon"]/span/text()').extract_first()

        return item
    
    def parseOverview(self, response):
        for sel in response.xpath('//ul[@class="listContent"]/li/div[@class="info"]'):
            yield self.parseOneItem(sel, response.meta['area'], response.meta['subarea'])

    def parseSubAreaPage(self, response):
        #print 'aaa', response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')
        pages = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()
        print ('bbb@@@',pages)
        if not pages:
            return
        totalPage = json.loads(pages)['totalPage']
        pageurl = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        for i in range(totalPage-1):
            url = ljurl + pageurl.replace('{page}', str(i+2))
            yield scrapy.Request(url, callback=self.parseOverview, meta={'area':response.meta['area'],
                                                                    'subarea':response.meta['subarea']},)
        for sel in response.xpath('//ul[@class="listContent"]/li/div[@class="info"]'):
            yield self.parseOneItem(sel, response.meta['area'], response.meta['subarea'])

    def parse(self, response):
        areas = response.xpath('//div[@data-role="ershoufang"]/div/a')
        i=0
        for area in areas:
            print ('area~~~', area)
            name = area.xpath('text()').extract_first()
            url = ljurl+area.xpath('@href').extract_first()
            
            yield scrapy.Request(url, meta={'area':name}, callback=self.parseArea)
            i+=1
            if i>3:
                break
            
    def parseArea(self, response):
        subareas = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')
        
        for subarea in subareas:
            print ('subare:',subarea)
            name = subarea.xpath('text()').extract_first()
            url = ljurl+subarea.xpath('@href').extract_first()
            
            yield scrapy.Request(url,callback=self.parseSubAreaPage, meta={'area':response.meta['area'],
                                                                    'subarea':name}, )
            break
        
    

class LianjiaCJSpider(scrapy.Spider):
    name = "ljcj"
    allowed_domains = ["lianjia.com"]
    start_urls = [ljurl+'/chengjiao/']
    
    def parseOneItem(self, sel, area, subarea):
        item = LianjiaCJItem()
        item['area'] = area
        item['subarea'] = subarea
        item['totalPrice'] = sel.xpath('div[@class="address"]/div[@class="totalPrice"]/span/text()').extract_first()

        item['title'] = sel.xpath('div[@class="title"]/a/text()').extract_first()
        item['dealDate'] = sel.xpath('div[@class="address"]/div[@class="dealDate"]/text()').extract_first()
        
        item['houseInfo'] = sel.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').extract_first()
        
        item['positionInfo']= sel.xpath('div[@class="flood"]/div[@class="positionInfo"]/text()').extract_first()
        item['source']= sel.xpath('div[@class="flood"]/div[@class="source"]/text()').extract_first()
        item['unitPrice']= sel.xpath('div[@class="flood"]/div[@class="unitPrice"]/span/text()').extract_first()

        return item
    
    def parseOverview(self, response):
        for sel in response.xpath('//ul[@class="listContent"]/li/div[@class="info"]'):
            yield self.parseOneItem(sel, response.meta['area'], response.meta['subarea'])

    def parseFirstPage(self, response):
        pages = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()
        totalPage = json.loads(pages)['totalPage']
        pageurl = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        for i in range(totalPage-1):
            url = ljurl + pageurl.replace('{page}', str(i+2))
            yield scrapy.Request(url, callback=self.parseOverview, meta={'area':response.meta['area'],
                                                                    'subarea':response.meta['subarea']},)
        for sel in response.xpath('//ul[@class="listContent"]/li/div[@class="info"]'):
            yield self.parseOneItem(sel, response.meta['area'], response.meta['subarea'])
            
    def parse(self, response):
        areas = response.xpath('//div[@data-role="ershoufang"]/div/a')
        for area in areas:
            name = area.xpath('text()').extract_first()
            url = ljurl+area.xpath('@href').extract_first()
            
            yield scrapy.Request(url, meta={'area':name}, callback=self.parseArea)
            
    def parseArea(self, response):
        subareas = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')
        for subarea in subareas:
            name = subarea.xpath('text()').extract_first()
            url = ljurl+subarea.xpath('@href').extract_first()
            
            yield scrapy.Request(url,callback=self.parseFirstPage, meta={'area':response.meta['area'],
                                                                    'subarea':name}, )
        
        

            

        
      
            