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
    list_display = ('.', 'deal_date','subarea','total_price',
                   'info','source','title','position_info',) # list

# Register your models here.
admin.site.register(City,NameUrlAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(SubArea,SubAreaAdmin)
admin.site.register(LjSecondChengjiaoRecord,LjSecondChengjiaoRecordAdmin)
admin.site.register(PullStatus,PullStatusAdmin)