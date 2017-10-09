from django.contrib import admin
from .models import *

class NameUrlAdmin(admin.ModelAdmin):
    list_display = ('name','url',) # list

class AreaAdmin(admin.ModelAdmin):
    list_display = ('name','city_name', 'url',) # list

    def city_name(self, obj):
        return obj.city.name
    city_name.admin_order_field = 'city__name'

class SubAreaAdmin(admin.ModelAdmin):
    list_display = ('name','area_name', 'area','url',) # list

    def area_name(self, obj):
        return obj.area.name
    area_name.admin_order_field = 'area__name'

class LjSecondChengjiaoRecordAdmin(admin.ModelAdmin):
    list_display = ('unit_price', 'deal_date','subarea','total_price',
                   'info','source','title','position_info',) # list
    list_per_page = 20
    list_filter = ('deal_date',)

class PullStatusAdmin(admin.ModelAdmin):
    list_display = ('type', 'subarea','total_pages','start_time',
                   'end_time',) # list

class PullPageStatusAdmin(admin.ModelAdmin):
    list_display = ('pull', 'url','finish_time','success_count',
                   'total_count',) # list
class LjSecondChengjiaoAdmin(admin.ModelAdmin):
    list_display = ('xiaoqu','subarea','unit_price', 'deal_date','total_price','floor_num','dianti',
                   'orientation','space','bedroom_num','meetingroom_num','produce_type','produce_date',
                    'other_info') # list
    def dianti(self, obj):
        if obj.elevator == 1:
            return '有电梯'
        elif obj.elevator == 0:
            return '无电梯'
        else:
            return '未知'
    list_per_page = 20
    list_filter = ('deal_date',)

# Register your models here.
admin.site.register(City,NameUrlAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(SubArea,SubAreaAdmin)
admin.site.register(LjSecondChengjiaoRecord,LjSecondChengjiaoRecordAdmin)
admin.site.register(PullStatus,PullStatusAdmin)
admin.site.register(PullPageStatus,PullPageStatusAdmin)
admin.site.register(LjSecondChengjiao,LjSecondChengjiaoAdmin)