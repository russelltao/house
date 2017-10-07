# -*- coding: utf-8 -*-s

from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib as mpl
from  datetime  import  *
import  time
mpl.matplotlib_fname() #将会获得matplotlib包所在文件夹

#mpl.use('Agg')

class LianjiaAnalyse(object):
    df= pd.read_csv('item.csv')
    areaList =["萧山","余杭","滨江","西湖"]
    df_xqPriuDate =pd.DataFrame()
    mon =[0,1,2,3,4,5,6,7,8,9,10,11,12] #0 represent 2015
    df_area_count=pd.DataFrame()
    df_area_priu=pd.DataFrame()
    df_subarea_count =pd.DataFrame()
    df_subarea_priu=pd.DataFrame()
    df_xq_count =pd.DataFrame()
    df_xq_priu=pd.DataFrame()

    def clearFalsePriceU(self, input_df,minPrice,MaxPrice):
        return  input_df[(input_df['priu']>=minPrice)&(input_df['priu']<=MaxPrice)]

    def anaByArea(self, area,suba=None,xq=None):
        df_area= self.df[self.df["area"]==area]
        g = df_area.groupby('suba')
        if xq:
            print '-------xq:', xq, '-------'
            df_xq = df_area[df_area['xq'] == xq]
            self.anaByXq(df_xq)
            ret_df_xq = df_xq
        if suba:
            print '#############subArea:', suba, '################'
            df_suba = df_area[df_area['suba'] == suba]
            self.anaBySubArea(df_suba,False)
            ret_df_xq = df_suba
        else:
            print '@@@@@@@@@@@@area:',area,'@@@@@@@@@@@@@@'
            print df_area[:1]
            a= df_area['suba'].describe()
            print a

            suba_list = df_area['suba'].drop_duplicates()
            for i in suba_list:
                print '###############subArea:', i, '##################'
                df_xq = df_area[df_area['suba'] == i]
                self.anaByXq(df_xq)
                break
            ret_df_xq = df_area
        return ret_df_xq

    def anaBySubaName(self, subaName,flag_xq=False):
        df_suba=pd.DataFrame()
        df_suba= self.df[self.df["suba"]==subaName]
        if len(df_suba)==0:
            print "wrong subaName!!"
            return None
        df_suba_cleared=self.clearFalsePriceU(df_suba, 7000, 50000)
        xq_list = df_suba['xq'].drop_duplicates()

        df_suba_des=  df_suba['xq'].describe()
        #print xq_list,df_suba_des
        for j in xq_list:
            df_xq =df_suba_cleared[(df_suba_cleared['xq'] == j)]
            if len(df_xq)<5:#少于5套的小区不分析
                print "less then 5"
                continue
            #list_xq ={j:[int(df_xq['priu'].mean())]}
            dict_xq_priu = df_xq[['xq','priu','date']]
            self.df_xqPriuDate= pd.concat([self.df_xqPriuDate,dict_xq_priu])
        print self.df_xqPriuDate
        xq_list = self.df_xqPriuDate['xq'].drop_duplicates()
        print xq_list
        #return xq_list,self.df_xqPriuDate
        self.showSuba_plot_byMon(xq_list,self.df_xqPriuDate)

    def showSuba_plot_byMon(self,list_xq_name,df_xq):
        font_size = 10  # 字体大小
        fig_size = (8, 6)  # 图表大小
        mpl.rcParams['font.size'] = font_size  # 更改默认更新字体大小
        mpl.rcParams['figure.figsize'] = fig_size  # 修改默认更新图表大小
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        bar_width = 0.35  # 设置柱形图宽度

        x=self.mon
        ylistCount={}
        ylistpriu={}

        for i in list_xq_name:
            ylistCount[i]=self.getYByMon(df_xq[df_xq['xq']==i])[0]
            ylistpriu[i]=self.getYByMon(df_xq[df_xq['xq']==i])[1]
        print ylistCount
        print ylistpriu

        #fig, ax = plt.subplots(nrows=2, ncols=2)

        plt.subplot(2, 1, 1)# （行，列，活跃区）
        plt.title(xq_name+' yCount & month')  # 添加图形标题
        plt.legend()  # 展示图例
        plt.xlabel('month')  # 给 x 轴添加标签
        plt.ylabel('yCount')  # 给 y 轴添加标签
        plt.plot(x, yCount, 'r-x', label='yCount')

        plt.subplot(2, 1, 2)
        plt.legend()  # 展示图例
        plt.xlabel('month')  # 给 x 轴添加标签
        plt.ylabel('priu')  # 给 y 轴添加标签
        plt.plot(x, yPriu, 'r-x', label='yPriu')

        plt.show()

    def anaBySubArea(self, df_suba,flag_xq=False):
        df_xq2=pd.DataFrame()
        df_area_cleared=self.clearFalsePriceU(df_suba, 7000, 50000)
        xq_list = df_area_cleared['xq'].drop_duplicates()
        a_xq=  xq_list.describe()
        print a_xq
        for j in xq_list:
            df_xq =df_area_cleared[(df_area_cleared['xq'] == j)]
            if flag_xq == True:
                self.anaByXq(df_xq)
                break
            else:
                if df_xq2.empty:
                    df_xq2 = self.df_init_count(xq_list)
                else:
                    print df_xq['priu'].mean()
                    df_squ_90 = self.getdf_spuare90(df_xq)
                    df_squ_140 = self.getdf_spuare140(df_xq)
                    yCount_90, yPriu_90 = self.getYCountfromXDate(self.mon, df_squ_90)
                    yCount_140, yPriu_140 = self.getYCountfromXDate(self.mon, df_squ_140)

    def anaByXq(self, df_xq):
        #xq_list = df_xq['xq'].drop_duplicates()
        #print xq_list.describe()
        #for j in xq_list:
        squ_90 = self.getdf_spuare90(df_xq)
        squ_140 = self.getdf_spuare140(df_xq)
        self.show_plot_byMonSqu(squ_90,squ_140)

    def df_init_count(self, xq_list):
        d_list = [[0]*12]*len(xq_list)
        df_count = pd.DataFrame(d_list,index = xq_list,columns= self.mon)
        #print df_count
        return df_count

    def getdf_spuare90(self,df_xq):
        xq_name = df_xq['xq'].drop_duplicates()
        a_90 = df_xq[df_xq['square'] <= 90]
        if a_90['suba'].count() > 0:
            print '----------------xq:', xq_name, '<=90----------------'
            a_90_priu = a_90['priu'].describe()
            a_90_data =a_90['date'].describe()
            print a_90_priu,a_90_data
        return a_90

    def getdf_spuare140(self, df_xq):
        xq_name = df_xq['xq'].drop_duplicates()
        a_140 = df_xq[(df_xq['square'] > 90) & (df_xq['square'] <= 140)]
        if a_140['suba'].count() > 0:
            print '----------------xq:', xq_name, '<=140----------------'
            a_140_priu= a_140['priu'].describe()
            a_140_data= a_140['date'].describe()
            print a_140_priu, a_140_data
        return a_140

    def dateCheck(self, date_str):
        date_stru=  time.strptime(date_str, "%Y-%m-%d")
        #print type(date_stru.tm_year)
        if date_stru.tm_year == 2015:
            return 0
        else:
            return date_stru.tm_mon

    def getYCountfromXDate(self,x_mon_list,df):
        yCount_list=[0]*13
        yPriU_list=[0]*13
        i=0
        #print df
        for index, row in df.iterrows():
            mon = self.dateCheck(row['date'])
            yCount_list[x_mon_list.index(mon)]+=1
            yPriU_list[x_mon_list.index(mon)]+=row['priu']

        while i <=12:
            if yCount_list[i]>1:
                yPriU_list[i]=yPriU_list[i]/yCount_list[i]
            i+=1

        return yCount_list,yPriU_list

    def getYByMonSqu(self,df_90,df_140):
        x=self.mon
        #index = pd.date_range('2016-01-01', '2016-12-30')
        #labels = df_xq['date'].drop_duplicates()
        #print labels
        yCount_90,yPriu_90 = self.getYCountfromXDate(x,df_90)
        yCount_140,yPriu_140 = self.getYCountfromXDate(x,df_140)
        return [yCount_90,yCount_140,yPriu_90,yPriu_140]

    def getYByMon(self,df):
        x=self.mon
        #index = pd.date_range('2016-01-01', '2016-12-30')
        #labels = df_xq['date'].drop_duplicates()
        #print labels
        yCount,yPriu = self.getYCountfromXDate(x,df)
        return [yCount,yPriu]



    def show1_plot_byMon(self,df_x):
        font_size = 10  # 字体大小
        fig_size = (8, 6)  # 图表大小
        mpl.rcParams['font.size'] = font_size  # 更改默认更新字体大小
        mpl.rcParams['figure.figsize'] = fig_size  # 修改默认更新图表大小
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        bar_width = 0.35  # 设置柱形图宽度

        x=self.mon
        #index = pd.date_range('2016-01-01', '2016-12-30')
        #labels = df_xq['date'].drop_duplicates()
        #print labels
        yCount=self.getYByMon(df_x)[0]
        yPriu=self.getYByMon(df_x)[1]
        xq_name = df_x['xq'].drop_duplicates()
        print xq_name
        #fig, ax = plt.subplots(nrows=2, ncols=2)

        plt.subplot(2, 1, 1)# （行，列，活跃区）
        plt.title(xq_name+' yCount & month')  # 添加图形标题
        plt.legend()  # 展示图例
        plt.xlabel('month')  # 给 x 轴添加标签
        plt.ylabel('yCount')  # 给 y 轴添加标签
        plt.plot(x, yCount, 'r-x', label='yCount')

        plt.subplot(2, 1, 2)
        plt.legend()  # 展示图例
        plt.xlabel('month')  # 给 x 轴添加标签
        plt.ylabel('priu')  # 给 y 轴添加标签
        plt.plot(x, yPriu, 'r-x', label='yPriu')

        plt.show()

    def show_plot_byMonSqu(self,df_squ_90,df_squ_140):
        font_size = 10  # 字体大小
        fig_size = (8, 6)  # 图表大小
        mpl.rcParams['font.size'] = font_size  # 更改默认更新字体大小
        mpl.rcParams['figure.figsize'] = fig_size  # 修改默认更新图表大小
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        bar_width = 0.35  # 设置柱形图宽度

        x=self.mon
        #index = pd.date_range('2016-01-01', '2016-12-30')
        #labels = df_xq['date'].drop_duplicates()
        #print labels
        yCount_90=self.getYByMonSqu(df_squ_90,df_squ_140)[0]
        yCount_140=self.getYByMonSqu(df_squ_90,df_squ_140)[1]
        yPriu_90=self.getYByMonSqu(df_squ_90,df_squ_140)[2]
        yPriu_140=self.getYByMonSqu(df_squ_90,df_squ_140)[3]
        xq_name = df_squ_90['xq'].drop_duplicates()
        print xq_name
        #fig, ax = plt.subplots(nrows=2, ncols=2)

        plt.subplot(2, 1, 1)# （行，列，活跃区）
        plt.title(xq_name+' yCount & month')  # 添加图形标题
        plt.legend()  # 展示图例
        plt.xlabel('month')  # 给 x 轴添加标签
        plt.ylabel('yCount')  # 给 y 轴添加标签
        plt.plot(x, yCount_90, 'r-x', label='yCount')
        plt.plot(x,yCount_140, 'b-+')

        plt.subplot(2, 1, 2)
        plt.legend()  # 展示图例
        plt.xlabel('month')  # 给 x 轴添加标签
        plt.ylabel('priu')  # 给 y 轴添加标签
        plt.plot(x, yPriu_90, 'r-x', label='yPriu')
        plt.plot(x, yPriu_140, 'b-+')

        plt.show()

def test1():
    a = LianjiaAnalyse()
    #a.anaByArea('滨江', '滨江区政府')
    a.anaBySubaName('滨江区政府')
if __name__ == "__main__":
    test1()