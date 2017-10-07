# -*- coding: utf-8 -*-s
#
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 50)
#print x
#plt.plot(x,np.sin(x))# 如果没有第一个参数 x，图形的 x 坐标默认为数组的索引
#plt.plot(x, np.sin(x),  x, np.sin(2 * x))
#plt.plot(x, np.sin(x), 'r-o',  x, np.cos(x), 'g--')
#plt.show()
#x = np.random.randn(1000)
#plt.hist(x, 50)

plt.plot(x, np.sin(x), 'r-x', label='Sin(x)')
plt.plot(x, np.cos(x), 'g-^', label='Cos(x)')
plt.legend() # 展示图例
plt.xlabel('Rads') # 给 x 轴添加标签
plt.ylabel('Amplitude') # 给 y 轴添加标签
plt.title('Sin and Cos Waves') # 添加图形标题
plt.show()