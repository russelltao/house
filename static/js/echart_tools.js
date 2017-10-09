/**
* Created by taohui on 2017/9/28.
*/

function create_pie(chart_id, title, legend, series) {
    var myChart = echarts.init(document.getElementById(chart_id));

    var option = {
        title: {
            text: title,
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : 'left',
            data:legend
        },
        toolbox: {
            show : true,
            orient: 'horizontal',      // 布局方式，默认为水平布局，可选为：
                           // 'horizontal' ¦ 'vertical'
            x: 'center',
            y: 'top',
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {
                    show: true,
                    type: ['pie', 'funnel']
                },
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        series: series
    };

    myChart.setOption(option);
}

        function create_chart(chart_id, title, legend, xAxis, series) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById(chart_id));

    // 指定图表的配置项和数据
    var option = {
        title: {
            text: title
        },
        tooltip: {},
        legend: {
            data:legend
        },
        xAxis: {
            data: xAxis
        },
        yAxis: {},
        series: series
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

        function create_plots(chart_id, title, legend, series) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById(chart_id));

    // 指定图表的配置项和数据
    var option = {
        backgroundColor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [{
            offset: 0,
            color: '#f7f8fa'
        }, {
            offset: 1,
            color: '#cdd0d5'
        }]),
        title: {
            text: title
        },
        legend: {
            right: 10,
            data: legend
        },
        xAxis: {
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
        },
        yAxis: {
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            scale: true
        },
        series:series
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
