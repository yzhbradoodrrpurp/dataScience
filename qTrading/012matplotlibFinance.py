# -*- coding = utf-8 -*-
# @Time: 2024/10/21 12:14
# @Author: Zhihang Yi
# @File: 012matplotlibFinance.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import random
import mplfinance as fin
from matplotlib.dates import date2num

"""
mplfinance 是一个用于绘制金融图表的 Python 库，专门设计用于处理和可视化金融数据，特别是股票、外汇和其他交易市场的数据。
它的主要功能包括：
蜡烛图：可以绘制蜡烛图，显示开盘价、最高价、最低价和收盘价，适合分析价格走势。
柱状图：支持绘制柱状图，用于显示价格变化。
成交量图：可以显示成交量，帮助分析市场活动。
自定义样式：允许用户自定义图表的样式，包括颜色、标签、标题等。
多种图表类型：支持多种类型的图表，如线图、柱状图、蜡烛图等，方便用户选择适合的可视化方式。
"""

stocks = pd.read_csv('008stocks.csv', index_col='date', parse_dates=True)
# 对DataFrame类型的stocks变量进行一些截取操作，去除不想要的数据。
stocks = stocks.iloc[:, 1:5]

# 'stocks.index' 表示得到stocks的行索引组成的列表。
# '.to_pydatetime()' 的作用是将pandas中的datetime类型转化为Python中的datetime类型。
# 'date2num()' 函数的作用时将Python中的datetime类型转换为matplotlib能够识别的浮点数，便于进行金融画图。
stocks['time'] = date2num(stocks.index.to_pydatetime())

# rename()方法能够对一个DataFrame类型的列索引进行变名操作。字典的键是原来的名字，值是改变之后的名字。
# 'inplace' 表示直接将变化作用于本身，而不用重新赋值给一个新变量。'inplace' 普遍存在于Series, DataFrame需要更改自身的方法之中。
stocks.rename(columns={'open': 'Open', 'close': 'Close', 'highest': 'High', 'lowest': 'Low'}, inplace=True)
print(stocks)

# '.plot()' 接收一个pandas中的DataFrame类型数据，同时要求这个数据必须包含 'Open' 'Close' 'High' 'Low' 列标签( 'Volume' 标签是可选择的)。
# 'type='candle'' 表示画的图的类型是蜡烛图(K线图)。
fin.plot(stocks, type='candle', volume=False)
