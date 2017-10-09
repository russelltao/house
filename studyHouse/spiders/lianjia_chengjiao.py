# coding=utf-8
import scrapy
from studyHouse.items import LianjiaCJItem, LianjiaZSItem
import json
import django
import datetime
django.setup()
from hdata.models import SubArea,LjSecondChengjiaoRecord,PullStatus,PullPageStatus
from django.db.models import Q


class LianjiaChengjiaoPagesSpider(scrapy.Spider):
    name = "lj_chengjiao_pages"
    allowed_domains = ["lianjia.com"]

    def __init__(self):
        hzurls_subarea = []
        startAreas = SubArea.objects.filter(area__city__name='杭州')
        for are in startAreas:
            url = are.url
            notfinish = True
            try:
                ps = PullStatus.objects.get(subarea=are, type='链家二手成交', end_time=None)
                allpps = PullPageStatus.objects.filter(Q(pull=ps), ~Q(finish_time=None))
                print('比较', ps, len(allpps))
                if len(allpps) >= ps.total_pages:
                    notfinish = False
                    ps.end_time = datetime.datetime.now()
                    ps.save()
            except PullStatus.DoesNotExist as e:
                pass

            if notfinish:
                url = url.replace('ershoufang', 'chengjiao')
                if url[0:4] == 'http':
                    hzurls_subarea.append(url)
                else:
                    hzurls_subarea.append(are.area.city.url + url)
            else:
                print('完成', are)
        print('start_urls个数', len(hzurls_subarea))
        LianjiaChengjiaoPagesSpider.start_urls = hzurls_subarea
        super(LianjiaChengjiaoPagesSpider).__init__()

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

        try:
            record.save()
            print('保存记录',record.total_price, record.title)
            return True
        except Exception as e:
            print(e)
            return False

    def parseOneResponse(self, subarea, response):
        try:
            pps = PullPageStatus.objects.get(pull__subarea=subarea,url=response.url,
                                             finish_time=None)
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
                    print('完成子区域',subarea,ps)
                return 1,ps
            return 0,ps
        except PullStatus.DoesNotExist as e:
            print(e)
            return -1,None

    def isPageFinish(self, url, ps):
        isFinished = False
        try:
            pps = PullPageStatus.objects.get(url=url, pull=ps)
            if pps.finish_time:
                print('页面已经完成',pps)
                isFinished = True
        except PullPageStatus.DoesNotExist as e:
            pps = PullPageStatus(url=url, pull=ps).save()

        return isFinished

    def parseOverview(self, response):
        self.parseOneResponse(response.meta['subarea'], response)

    def parse(self, response):
        for i in range(len(LianjiaChengjiaoPagesSpider.start_urls)):
            if LianjiaChengjiaoPagesSpider.start_urls[i] == response.url:
                break

        myarea = startAreas[i]

        pages = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()
        totalPage = json.loads(pages)['totalPage']
        pageurl = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()

        res,ps = self.isFinish(myarea)
        print(i, myarea, '页面isFinish',res, ps)
        if res == 1:
            return
        elif res == -1:
            ps = PullStatus(subarea=myarea, type='链家二手成交', start_time=datetime.datetime.now(),
                            total_pages=totalPage, )
            ps.save()
        for i in range(totalPage - 1):
            url = myarea.area.city.url + pageurl.replace('{page}', str(i + 2))
            isFinished = self.isPageFinish(url,ps)
            if not isFinished:
                yield scrapy.Request(url, callback=self.parseOverview, meta={'subarea':myarea}, )
        if not self.isPageFinish(response.url,ps):
            self.parseOneResponse(myarea, response,)


