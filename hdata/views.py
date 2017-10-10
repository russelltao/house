from django.shortcuts import render
from django.views.generic import TemplateView
from .models import LjSecondChengjiao
from django.db.models import Count, Min, Sum, Avg,StdDev,Max
from pyecharts import Line


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

        day_attrs = [dc['deal_date'].strftime('%Y%m%d') for dc in alldays]

        unitprice_byarea_line = Line(title="二手房区域日成交均价趋势",subtitle='杭州地区各行政区域统计',
                    width=1800)
        for k,v in unitprice_series.items():
            unitprice_byarea_line.add("%s"%(k), day_attrs, v, mark_point=["average"])

        dealcnt_byarea_line = Line(title="二手房区域日成交次数趋势",subtitle='杭州地区各行政区域统计',
                    width=1800)
        for k,v in sellcnt_series.items():
            dealcnt_byarea_line.add("%s"%(k), day_attrs, v, mark_point=["average"])

        totalprice_byarea_line = Line(title="二手房区域日成交次数趋势",subtitle='杭州地区各行政区域统计',
                    width=1800)
        for k,v in totalprice_sum_series.items():
            totalprice_byarea_line.add("%s"%(k), day_attrs, v, mark_point=["average"])

        attr = []
        unitPriceAvg = []
        unitPriceMax = []
        dealCnt = []
        totalpriceSum = []
        ljcj_stats = LjSecondChengjiao.objects.values('deal_date') \
            .annotate(Count('id'),Avg('unit_price'),Max('unit_price'),Sum('total_price'),).order_by('deal_date')
        for ls in ljcj_stats:
            attr.append(ls['deal_date'])
            unitPriceAvg.append(ls['unit_price__avg'])
            unitPriceMax.append(ls['unit_price__max'])
            dealCnt.append(ls['id__count'])
            totalpriceSum.append(ls['total_price__sum'])

        unitprice_line = Line(title="二手房日成交均价趋势",subtitle='杭州地区链家数据统计',
                    width=1800)
        unitprice_line.add("单价均价", attr, unitPriceAvg, mark_point=["average"])
        unitprice_line.add("单价最高价", attr, unitPriceMax, mark_point=["average"])

        dealcnt_line = Line(title="二手房日成交次数趋势",subtitle='杭州地区链家数据统计',
                    width=1800)
        dealcnt_line.add("成交次数", attr, dealCnt, )

        totalprice_line = Line(title="二手房日成交总价趋势",subtitle='杭州地区链家数据统计',
                    width=1800)
        totalprice_line.add("总价", attr, dealCnt, )

        context['unitprice_line'] = unitprice_line.render_embed()
        context['dealcnt_line'] = dealcnt_line.render_embed()
        context['unitprice_byarea_line'] = unitprice_byarea_line.render_embed()
        context['dealcnt_byarea_line'] = dealcnt_byarea_line.render_embed()
        context['totalprice_byarea_line'] = totalprice_byarea_line.render_embed()
        context['totalprice_line'] = totalprice_line.render_embed()

        context['host'] = 'http://localhost:8000'
        context['script_list'] = unitprice_line.get_js_dependencies()+ \
                                 unitprice_byarea_line.get_js_dependencies()+ \
                                 dealcnt_byarea_line.get_js_dependencies()+\
                                 dealcnt_line.get_js_dependencies()+\
                                 totalprice_line.get_js_dependencies()

        return context
