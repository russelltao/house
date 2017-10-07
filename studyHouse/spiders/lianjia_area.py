# coding=utf-8
import scrapy
from studyHouse.items import LianjiaCJItem, LianjiaZSItem
import json

ljurl = 'https://hz.lianjia.com'
hzarea2 = ['binjiang', 'xihu', 'xiacheng', 'jianggan', 'gongshu', 'shangcheng', 'yuhang', 'xiaoshan']
hzarea = ['binjiang']

hzurlzs, hzurlcj = [], []
for area in hzarea:
    hzurlzs.append('%s/ershoufang/%s' % (ljurl, area))

import django
django.setup()
from hdata.models import City,Area,SubArea

class LianjiaAreaSpider(scrapy.Spider):
    name = "lj_area"
    allowed_domains = ["lianjia.com"]
    start_urls = [ljurl]#+'/ershoufang/'

    def parse(self, response):
        areas = response.xpath('//div[@class="city-enum fl"]/a')
        i = 0
        for area in areas:
            print('city~~~', area)
            name = area.xpath('text()').extract_first()
            url = area.xpath('@href').extract_first()
            print(name,url)
            try:
                exist = City.objects.get(name=name)
                print(exist)
                exist.name = name
                exist.url = url
                exist.save()
            except City.DoesNotExist as e:
                exist= City(name=name,url=url).save()

            if url[0:10] != 'http://you':
                # 二手房里找子区域
                yield scrapy.Request(url + 'ershoufang/',
                                     meta={'name': name, 'city': exist},
                                     callback=self.parseArea)

    def parseArea(self, response):
        mycity = response.meta['city']
        subareas = response.xpath('//div[@data-role="ershoufang"]/div/a')

        for subarea in subareas:
            print('area:', subarea)
            name = subarea.xpath('text()').extract_first()
            url = subarea.xpath('@href').extract_first()
            print(name,url)
            try:
                exist = Area.objects.get(name=name,city=mycity)
                exist.name = name
                exist.url = url
                exist.save()
                print(exist)
            except Area.DoesNotExist as e:
                exist = Area(name=name,url=url,city=mycity).save()

hzurls_subarea = []
startAreas = Area.objects.filter(city__name='杭州')
for are in startAreas:
    if are.url[0:4] == 'http':
        hzurls_subarea.append(are.url)
    else:
        hzurls_subarea.append(are.city.url+are.url)
print (hzurls_subarea)
class LianjiaSubAreaSpider(scrapy.Spider):
    name = "lj_subarea"
    allowed_domains = ["lianjia.com"]
    start_urls = hzurls_subarea
    def parse(self, response):
        for i in range(len(LianjiaSubAreaSpider.start_urls)):
            if LianjiaSubAreaSpider.start_urls[i] == response.url:
                break
        print(i,startAreas[i])
        myarea = startAreas[i]
        subareas = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')

        for subarea in subareas:
            print('area:', subarea)
            name = subarea.xpath('text()').extract_first()
            url = subarea.xpath('@href').extract_first()
            print(name,url)
            try:
                exist = SubArea.objects.get(name=name,area=myarea)
                print(exist)
            except SubArea.DoesNotExist as e:
                SubArea(name=name,url=url,area=myarea).save()
