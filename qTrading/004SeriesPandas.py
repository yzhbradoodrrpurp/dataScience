# -*- coding = utf-8 -*-
# @Time: 2024/10/18 16:42
# @Author: Zhihang Yi
# @File: 004SeriesPandas.py
# @Software: PyCharm

"""
NumPy是Python数据分析中的基础模块，用于进行各种数学运算、批量运算。
pandas是Python数据分析中的核心模块，用于操纵结构化的数据(数据清洗、转换、分析、可视化)。
"""

import pandas as pd
import random

"""
Series是pandas中的一种数据类型，类似于一维列表(或者是与字典的结合)，
由一组数据和一组与之相关的数据标签(索引)组成。
"""
# 创建Series使用pd.Series([...])，索引默认为从0开始的数字。
a = pd.Series([2, 3, 5, 4])
print(a)
# 可以给Series类型数据加上索引，要求索引的个数必须和数据的个数相同。
# pd.Series([..], index=[...])
a = pd.Series([2, 3, 5, 4], index=['a', 'b', 'c', 'd'])
print(a)

# pd.Series(...)也可以直接接收一个list, ndarray，在此不再演示。

# Series的索引可以用自定义的index，也可以使用从0开始的整数，引用方式和list, ndarray相同。
# 同样Series也可以进行切片，在这里不再演示。
print(a['a'])

# 相同长度/不同长度的Series可以进行加减乘除，相同的索引下的数值进行加减乘除。
# 两个Series中有不同的索引，加减乘除后这个索引下的值为NaN。
b = pd.Series([5, 16, 2, 9], index=['a', 'b', 'c', 'd'])
print(a + b)

# 如果不想出现NaN，而是没出现的索引的值用0代替，那么就可以使用.add(), .sub(), .mul(), .div()。
# 同时将fill_value参数设为0.
a = pd.Series([random.randint(-10, 10) for i in range(4)], index=['a', 'b', 'c', 'd'])
b = pd.Series([random.randint(-5, 5) for i in range(2)], index=['b', 'c'])
c = a.add(b, fill_value=0)
print(c)

# 可以用.isnull(), null()判断Series上的行是不是NaN，返回一个bool类型数据。
c = a + b
print(c.isnull(), c.notnull())

# 可以用.dropna()去除NaN，.fillna(...)给NaN赋值。
c = a + b
c = c.dropna()
print(c)
c = a + b
c = c.fillna(0)
print(c)

# 可以通过列表创建Series，也能通过字典直接创建Series。
l = [1, 3, 6, 2, 7]
a = pd.Series(l)
print(a)
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
a = pd.Series(d)
print(a)

# Series类型变量也能进行布尔过滤。
a = pd.Series([random.uniform(-10, 10) for i in range(20)])
print(a)
a = a[a > 0]
print(a)

# Series类型和ndarray一样，在深复制时要使用.copy()方法。

# 在用整数作为索引时，在切片之后会出现一些数值上不好进行索引的地方。
# 这个时候推荐使用loc[], iloc[]。
# loc[...] 得到标签为...的元素，iloc[]得到行数为...的元素。
# loc[...]可以接收整数和字符串，但是iloc[]只能接收整数。

