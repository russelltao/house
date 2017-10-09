# -*- coding: utf-8 -*-

import csv
import django
import re,os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "house.settings")
django.setup()
from hdata.models import LjSecondChengjiao,LjSecondChengjiaoRecord
from django.db.models import Q

LjSecondChengjiao.objects.all().delete()

newrows=[]
allRecords = LjSecondChengjiaoRecord.objects.all()
for row in allRecords:
    newrow = LjSecondChengjiao(unit_price=row.unit_price, total_price=row.total_price,
                               subarea=row.subarea,deal_date=row.deal_date,
                               source=row.source,)
    floors = re.findall(r'共(\d+)层.*(\d{4})年建(.+)', row.position_info)
    normal = [False,False,False,False]
    if len(floors) == 0:
        floors = re.findall(r'共(\d+)层.*(\d{4})年建', row.position_info)
        if len(floors) == 0:
            floors = re.findall(r'共(\d+)层.{2}(.+)', row.position_info)
            if len(floors) == 0:
                floors = re.findall(r'共(\d+)层', row.position_info)
                if len(floors) == 0:
                    print ('error floor',row.position_info)
                    fn = 0
                else:
                    fn = floors[0]
                    print ('floor only tf:',row.position_info)
            else:
                fn,newrow.produce_type = floors[0]
                print ('floor only tf and typ:',row.position_info)
        else:
            fn,newrow.produce_date = floors[0]

            print ('floor only tf year:',row.position_info)
    else:
        normal[0] = True
        fn,newrow.produce_date,newrow.produce_type = floors[0]
    newrow.floor_num = int(fn)

    title = re.findall(r'(.*) (\d+)室(\d+)厅 ([\d.]+)平米', row.title)
    snum,tnum = 0,0
    if len(title) == 0:
        print ('title error:',row.title)
        title = re.findall(r'(.*) --室--厅 ([\d.]+)平米', row.title)
        try:
            newrow.xiaoqu,newrow.space = title[0]
        except IndexError as e:
            print (e)
            print ('未处理',title)
    else:
        normal[1] = True
        newrow.xiaoqu,bn,mn,newrow.space = title[0]
        newrow.bedroom_num = int(bn)
        newrow.meetingroom_num = int(mn)

    #title = re.findall(r'(.*)电梯', row[5])
    try:
        newrow.orientation,newrow.other_info,dt = row.info.split('|')
        if dt.find('有电梯') != -1:
            newrow.elevator = True
        elif dt.find('无电梯') != -1:
            newrow.elevator = False
        else:
            print('电梯错误：',dt)
        normal[2] = True
    except ValueError as e:
        print (e,'电梯改为None',row.info)
        newrow.orientation, newrow.other_info = row.info.split('|')

    try:
        if row.unit_price < 100:
            print ('strange',row.unit_price)
        else:
            normal[3] = True
    except ValueError:
        pass

    n = True
    for nm in normal:
        n = n and nm

    if not n:
        print(normal)
        print(newrow)
    try:
        newrow.save()
    except Exception as e:
        print(e)
        
headers = ['area','suba','xq','prit','priu','date','floor','square','snum','tnum','cx','zx','dt','src','year','typ']
print(newrows)
    