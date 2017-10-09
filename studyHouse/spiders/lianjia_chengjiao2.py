# coding=utf-8
import scrapy
from studyHouse.items import LianjiaCJItem, LianjiaZSItem
import json
import django
import datetime
django.setup()
from hdata.models import SubArea,LjSecondChengjiaoRecord,PullStatus,PullPageStatus
from django.db.models import Q


class LianjiaChengjiao2Spider(scrapy.Spider):
    name = "lj_chengjiao2"
    allowed_domains = ["lianjia.com"]

    def __init__(self):
        hzurls_subarea = []
        self.detail_list = []
        now = datetime.datetime.now()

        url_dict = {}
        allpps = PullPageStatus.objects.filter(finish_time=None)
        for pps in allpps:
            if pps.pull.end_time is not None:
                pps.finish_time = pps.pull.end_time
                pps.save()
                print('异常',pps)
            else:
                url_dict[pps.url] = pps

        for k, v in url_dict.items():
            hzurls_subarea.append(k)
            self.detail_list.append(v)
        print('start_urls个数', len(hzurls_subarea),len(allpps))
        LianjiaChengjiao2Spider.start_urls = hzurls_subarea
        super(LianjiaChengjiao2Spider).__init__()

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

    def parseOneResponse(self, pps, response):
        total = 0
        success = 0
        for sel in response.xpath('//ul[@class="listContent"]/li/div[@class="info"]'):
            if self.parseOneItem(sel, pps.pull.subarea):
                success+=1
            success+=1
        pps.total_count+=total
        pps.success_count+=success
        pps.finish_time = datetime.datetime.now()
        pps.save()

        self.isFinish(pps)

    def isFinish(self, pps):
        try:
            ps = pps.pull
            allpps_cnt = PullPageStatus.objects.filter(~Q(finish_time=None)).count()
            if allpps_cnt >= ps.total_pages:
                if not ps.end_time:
                    ps.end_time = datetime.datetime.now()
                    ps.save()
                    print('完成子区域',ps)
                return 1,ps
            else:
                print('还差',ps.total_pages-allpps_cnt,ps)
            return 0,ps
        except PullStatus.DoesNotExist as e:
            print(e)
            return -1,None

    def parse(self, response):
        for i in range(len(LianjiaChengjiao2Spider.start_urls)):
            if LianjiaChengjiao2Spider.start_urls[i] == response.url:
                break

        pps = self.detail_list[i]
        self.parseOneResponse(pps, response,)


