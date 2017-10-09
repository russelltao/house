from django.shortcuts import render
from django.views.generic import TemplateView
from .models import LjSecondChengjiao
from django.db.models import Count, Min, Sum, Avg,StdDev,Max

# Create your views here.
class OverviewStatView(TemplateView):
    template_name = "overview.html"

    def get_context_data(self, **kwargs):
        context = super(OverviewStatView, self).get_context_data(**kwargs)
        ljcj_cnts = LjSecondChengjiao.objects.values('deal_date','subarea__area__name') \
            .annotate(Count('id'),Avg('unit_price'),Sum('total_price'),).order_by('deal_date')
        cnt_series = {}

        alldays = LjSecondChengjiao.objects.values('deal_date').order_by('deal_date').distinct()
        print(alldays)
        codes = {}
        day_code_api_series = {}
        for dcasr in ljcj_cnts:
            code = dcasr['subarea__area__name']
            day = dcasr['deal_date']
            cnt = dcasr['id__count']
            unit_price__avg = dcasr['unit_price__avg']
            sumtotal_price = dcasr['total_price__sum']
            codes[code] = 1
            if code in day_code_api_series:
                day_code_api_series[code][day] = [cnt, unit_price__avg, sumtotal_price]
            else:
                day_code_api_series[code] = {day: [cnt, unit_price__avg, sumtotal_price]}
        sellcnt_series = {}
        unitprice_series = {}
        totalprice_sum_series = {}
        for code, v in codes.items():
            unitprice_series[code] = []
            sellcnt_series[code] = []
            totalprice_sum_series[code] = []
            for d in alldays:
                day = d['deal_date']
                cnt = 0
                unit_price__avg = 0
                totalprice = 0
                if code in day_code_api_series:
                    if day in day_code_api_series[code]:
                        cnt = day_code_api_series[code][day][0]
                        unit_price__avg = day_code_api_series[code][day][1]
                        totalprice = day_code_api_series[code][day][2]

                sellcnt_series[code].append(cnt)
                unitprice_series[code].append(unit_price__avg)
                totalprice_sum_series[code].append(totalprice)

        context['ljcj_cnt_by_dealdate'] = {
                'series': sellcnt_series,
                'xAxis': [dc['deal_date'].strftime('%Y%m%d') for dc in alldays]
        }

        context['ljcj_unitprice_by_dealdate'] = {
                'series': unitprice_series,
                'xAxis': [dc['deal_date'].strftime('%Y%m%d') for dc in alldays]
        }
        context['ljcj_totalprice_by_dealdate'] = {
                'series': totalprice_sum_series,
                'xAxis': [dc['deal_date'].strftime('%Y%m%d') for dc in alldays]
        }

        return context
