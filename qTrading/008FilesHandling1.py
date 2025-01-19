# -*- coding = utf-8 -*-
# @Time: 2024/10/20 14:17
# @Author: Zhihang Yi
# @File: 008FilesHandling1.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import random
from datetime import datetime


# 用pd.read.csv('...')读取一个.csv文件的数据，然后传递给一个DataFrame变量。
stocks = pd.read_csv('008stocks.csv')
print(stocks)

print()

# 可以用read.csv('...')中的参数index_col指定哪一列为索引，可以用列数也可以用列名。
stocks = pd.read_csv('008stocks.csv', index_col=0)
print(stocks)
stocks = pd.read_csv('008stocks.csv', index_col='date')
print(stocks)

# 如果以日期为索引的话，日期的类型是str，不是datetime，那么就无法使用resample()等方法。
# 这个时候可以用parse_dates参数进行调整。
# 对parse_dates赋值为True，就会将所有能解释为datetime的数解释为datetime。
# 也可以对parse_dates赋值一个列(列数/列名)，那么就会将这一个列解释为datetime。
stocks = pd.read_csv('008stocks.csv', index_col='date', parse_dates=True)
print(stocks)

# 由于.csv文件会默认第一行就是各列的列名，所以有可能遇到文件从第一行开始就是数据而没有列名的情况。
# 这个时候我们可以手动添加列名。
# 'header=None' 表示这个.csv文件没有标题, 'names = [...]' 表示给各列加上标题，标题数要和列数相符合。
stocks1 = pd.read_csv('008stocks1.csv', header=None, names=['row', 'date', 'open', 'close', 'highest', 'lowest'])
print(stocks1)

# 有时候文件的数据会缺失，出现'None', 'nan'等字符串。
# 这个时候我们希望字符串能够解释为 'NaN'(浮点数类型)。
# 这个时候我们可以用na_values=[...]
stocks1 = pd.read_csv('008stocks1.csv', na_values=['none', 'None', 'NaN', 'nan'], header=None, names=['row', 'date', 'open', 'close', 'highest', 'lowest'])
print(stocks1)

#
