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
    def __str__(self):              # __unicode__ on Python 2
        return "%s(%s %s)"%(self.subarea,self.total_pages, self.start_time)

class PullPageStatus(models.Model):
    pull = models.ForeignKey(PullStatus)
    url = models.URLField()
    finish_time = models.DateTimeField(null=True)
    success_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('pull', 'url',)
        verbose_name = "拉取页面状态表"
    def __str__(self):              # __unicode__ on Python 2
        return "%s(%s %s)"%(self.pull,self.url, self.finish_time)

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

class LjSecondChengjiao(models.Model):
    subarea = models.ForeignKey(SubArea,verbose_name='区域')
    total_price = models.FloatField(verbose_name='总价（万）')
    deal_date = models.DateField(verbose_name='交易日期')
    source = models.CharField(max_length=200,verbose_name='来源')
    xiaoqu = models.CharField(max_length=100,verbose_name='小区名')
    bedroom_num = models.IntegerField(verbose_name='室',default=-1)
    meetingroom_num = models.IntegerField(verbose_name='厅',default=-1)
    space = models.FloatField(verbose_name='面积（平方米）')
    floor_num = models.IntegerField(verbose_name='总层数',default=-1)
    produce_date = models.IntegerField(null=True,verbose_name='建筑年份')
    produce_type = models.CharField(max_length=100, verbose_name='建筑类型')
    elevator = models.IntegerField(default=-1,verbose_name='电梯')
    orientation = models.CharField(max_length=10, verbose_name='朝向')
    other_info = models.CharField(max_length=100, verbose_name='其他信息')
    unit_price = models.IntegerField(verbose_name='单价')

    class Meta:
        unique_together = ('unit_price', 'space', 'deal_date','subarea','xiaoqu')
        verbose_name = "链家二手房成交表"
    def __str__(self):              # __unicode__ on Python 2
        return "[%s] %s %s %s %d室%d厅 %d层楼 建筑年代：%s 建筑类型：%s 电梯%s 朝向：%s"%(self.subarea,self.xiaoqu, self.produce_type,
            self.other_info,self.bedroom_num,self.meetingroom_num,self.floor_num,
            self.produce_date,self.produce_type, self.elevator, self.orientation)