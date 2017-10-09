python爬虫

#1、拉取链家区域数据
* scrapy crawl lj_area 
* scrapy crawl lj_subarea
* scrapy crawl lj_chengjiao

#2、如何可视化？
django admin
* df = pd.read_csv('c_ljcj.csv')
* df2 = df.set_index('date')
* df2.index = pd.to_datetime(df2.index)
* df2['priu'].plot()