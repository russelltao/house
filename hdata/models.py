# coding=utf-8

from django.db import models


class City(models.Model):
    name = models.CharField(verbose_name='城市名称',unique=True,max_length=20)
    url = models.URLField(verbose_name='访问地址',null=True)

    class Meta:
        verbose_name = "城市"
    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Area(models.Model):
    city = models.ForeignKey(City, verbose_name='城市')
    name = models.CharField(verbose_name='区域名称',max_length=20)
    url = models.URLField(null=True)

    class Meta:
        verbose_name = "二手房行政区域"
        unique_together = ('city', 'name')
    def __str__(self):              # __unicode__ on Python 2
        return "[%s]%s"%(self.city,self.name)

class SubArea(models.Model):
    area = models.ForeignKey(Area)
    name = models.CharField(verbose_name='子区域名称',max_length=30)
    url = models.URLField(null=True)

    class Meta:
        unique_together = ('area', 'name')
        verbose_name = "二手房子区域"
    def __str__(self):              # __unicode__ on Python 2
        return "%s(%s)"%(self.area,self.name)

class PullStatus(models.Model):
    subarea = models.ForeignKey(SubArea)
    type = models.CharField(max_length=100)
    total_pages = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('subarea', 'type', 'start_time')
        verbose_name = "拉取状态表"

class PullPageStatus(models.Model):
    pull = models.ForeignKey(PullStatus)
    url = models.URLField()
    finish_time = models.DateTimeField(null=True)
    success_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('pull', 'url',)
        verbose_name = "拉取页面状态表"

#95,低楼层(共30层) 2014年建塔楼,大学城北,江干,2016.10.24,南 | 其他,链家成交,杭州碧桂园 3室2厅 89平米,10675
class LjSecondChengjiaoRecord(models.Model):
    subarea = models.ForeignKey(SubArea)
    total_price = models.FloatField()
    position_info = models.CharField(max_length=200)
    deal_date = models.DateField()
    info = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    unit_price = models.IntegerField()
    class Meta:
        unique_together = ('unit_price', 'title', 'deal_date','total_price')
        verbose_name = "链家二手房成交记录"
