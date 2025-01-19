# -*- coding = utf-8 -*-
# @Time: 2024/10/20 15:45
# @Author: Zhihang Yi
# @File: 009matplotlibBasics.py
# @Software: PyCharm

import numpy as np
from numpy import pi
import pandas as pd
from matplotlib import pyplot as plt


# plt.plot()是用于画图的，plt.show()是用于展示画图的。
plt.plot()
plt.show()

# 具体地来说，plot()是用于画折线图的。
# 给出两个list/ndarray(要求长度相同)，
# 将列表中的元素一一对应地在Oxy平面画出并按照顺序连起来。
plt.plot([2, 4, 6, 8], [4, 7, 12, 15])
plt.show()

# 可以对plt.plot()传入特定的参数，改变点线的格式、颜色等等。
x = np.linspace(-np.pi/2, np.pi/2, 10)
y = np.sin(x)
# 'o-' 表示标出点和线。
plt.plot(x, y, 'o-')
plt.show()
# '--' 表示虚线。
x = np.linspace(-10, 10, 1000)
y = x**2
plt.plot(x, y, '--')
plt.show()
# 'r' 表示用红线绘画。
x = np.linspace(0, 5, 10000)
y = np.exp(x)
plt.plot(x, y, 'r')
plt.show()

# 可以在同一张图中画出多条线，只用在plt.show()之前多用几次plt.plot()。
x = np.linspace(0, 3, 10000)
y1 = np.sqrt(x)
y2 = np.pow(x, 2)
plt.plot(x, y1, 'r')
plt.plot(x, y2, 'g')
plt.show()

# 可以对一个图加上标题，对x、y分别添加描述。
x = np.linspace(0.1, 1, 100)
y1 = np.tan(x)
y2 = np.arctan(x)
plt.plot(x, y1, '--r')
plt.plot(x, y2, '--b')
# 用plt.title('...')添加标题。
plt.title('This is the title.')
# 用plt.xlabel('...'), plt.ylabel('...')设置x, y轴的标签。
plt.xlabel('This is the x-axis.')
plt.ylabel('This is the y-axis.')
plt.show()

# 我们也可以对x, y轴展示出的范围进行设置。
x = np.linspace(0, 10, 1000)
y1 = np.sqrt(x)
y2 = np.cos(x)
plt.plot(x, y1, '--r')
plt.plot(x, y2, '--b')
# plt.xlim(...), plt.ylim(...)接收两个数字，对展示出的x, y轴范围进行设置。
plt.xlim(0, 3)
plt.ylim(0, 2)
plt.show()

# plt.xticks(), plt.yticks()接收一个list/tuple/ndarray，设置x, y轴的刻度。
x = np.linspace(-10, 10, 100)
y1 = np.sqrt(100 - x**2)
y2 = -np.sqrt(100 - x**2)
plt.plot(x, y1, 'r')
plt.plot(x, y2, 'r')
plt.xticks(np.arange(0, 10, 5))
plt.yticks(np.arange(0, 10, 5))
plt.show()

# plt.legend()可以添加图例，但是要先在每个图的加上label。
x = np.linspace(-10, 10, 10000)
y1 = np.pow(x, 2)
y2 = np.pow(x, 3)
plt.plot(x, y1, 'r', label='y=x**2')
plt.plot(x, y2, 'b', label='y=x**3')
plt.legend()
plt.xlim(-10, 10)
plt.ylim(-50, 50)
plt.xticks(np.arange(-10, 10, 5))
plt.yticks(np.arange(-50, 50, 5))
plt.show()

# matplotlib也支持从Series, DatFrame类型数据直接进行画图。
stocks = pd.read_csv('008stocks.csv', index_col='date', parse_dates=True).iloc[:, 1:5]
stocks.plot()
plt.show()
