# coding=utf-8
import scrapy
from studyHouse.items import LianjiaCJItem, LianjiaZSItem
import json
import django
import datetime
django.setup()
from hdata.models import SubArea,LjSecondChengjiaoRecord,PullStatus,PullPageStatus
from django.db.models import Q

hzurls_subarea = []
startAreas = SubArea.objects.filter(area__city__name='杭州')
for are in startAreas:
    url = are.url
    notfinish = True
    try:
        ps = PullStatus.objects.get(subarea=are, type='链家二手成交', end_time=None)
        allpps = PullPageStatus.objects.filter(~Q(finish_time=None))
        if len(allpps) == ps.total_pages:
            notfinish = False
    except PullStatus.DoesNotExist as e:
        pass

    if notfinish:
        url = url.replace('ershoufang','chengjiao')
        if url[0:4] == 'http':
            hzurls_subarea.append(url)
        else:
            hzurls_subarea.append(are.area.city.url+url)

print (hzurls_subarea)
class LianjiaChengjiaoSpider(scrapy.Spider):
    name = "lj_chengjiao"
    allowed_domains = ["lianjia.com"]
    start_urls = hzurls_subarea

    def parseOneItem(self, sel, subarea):
        record = LjSecondChengjiaoRecord()
        record.subarea = subarea
        record.total_price = sel.xpath(
            'div[@class="address"]/div[@class="totalPrice"]/span/text()').extract_first()

        record.title = sel.xpath('div[@class="title"]/a/text()').extract_first()
        record.deal_date = datetime.datetime.strptime(\
            sel.xpath('div[@class="address"]/div[@class="dealDate"]/text()').extract_first(),
        "%Y.%m.%d")

        record.info = sel.xpath(
            'div[@class="address"]/div[@class="houseInfo"]/text()').extract_first()

        record.position_info = sel.xpath(
            'div[@class="flood"]/div[@class="positionInfo"]/text()').extract_first()
        record.source = sel.xpath('div[@class="flood"]/div[@class="source"]/text()').extract_first()
        record.unit_price = sel.xpath(
            'div[@class="flood"]/div[@class="unitPrice"]/span/text()').extract_first()
        print(record.total_price, record.title)
        try:
            record.save()
            return True
        except Exception as e:
            print(e)
            return False

    def parseOneResponse(self, subarea, response):
        try:
            pps = PullPageStatus.objects.get(subarea=subarea, type='链家二手成交', end_time=None)
        except PullPageStatus.DoesNotExist as e:
            print(e)
            raise e

        total = 0
        success = 0
        for sel in response.xpath('//ul[@class="listContent"]/li/div[@class="info"]'):
            if self.parseOneItem(sel, subarea):
                success+=1
            success+=1
        pps.total_count+=total
        pps.success_count+=success
        pps.finish_time = datetime.datetime.now()
        pps.save()

        self.isFinish(subarea)


    def isFinish(self, subarea):
        try:
            ps = PullStatus.objects.get(subarea=subarea, type='链家二手成交', end_time=None)
            allpps = PullPageStatus.objects.filter(~Q(finish_time=None))
            if len(allpps) == ps.total_pages:
                if not ps.end_time:
                    ps.end_time = datetime.datetime.now()
                    ps.save()
                return True
        except PullStatus.DoesNotExist as e:
            print(e)
        return False

    def parseOverview(self, response):
        self.parseOneResponse(response.meta['subarea'], response)

    def parse(self, response):
        for i in range(len(LianjiaChengjiaoSpider.start_urls)):
            if LianjiaChengjiaoSpider.start_urls[i] == response.url:
                break
        print(i, startAreas[i])
        myarea = startAreas[i]

        pages = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()
        totalPage = json.loads(pages)['totalPage']
        pageurl = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()

        if self.isFinish(myarea):
            return
        else:
            ps = PullStatus(subarea=myarea, type='链家二手成交', start_time=datetime.datetime.now(),
                            total_pages=totalPage, )
            ps.save()
        for i in range(totalPage - 1):
            url = myarea.area.city.url + pageurl.replace('{page}', str(i + 2))
            isFinished = False
            try:
                pps = PullPageStatus.objects.get(url=url,pull=ps)
                if pps.finish_time:
                    print(pps)
                    isFinished = True
            except PullPageStatus.DoesNotExist as e:
                pps = PullPageStatus(url=url,pull=ps).save()
            print(url,i,totalPage,isFinished)
            if not isFinished:
                yield scrapy.Request(url, callback=self.parseOverview, meta={'subarea':myarea}, )

        self.parseOneResponse(myarea, response,)


