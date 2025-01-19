# -*- coding = utf-8 -*-
# @Time: 2024/10/15 16:56
# @Author: Zhihang Yi
# @File: 003numPyCalculation.py
# @Software: PyCharm

import numpy as np
from numpy import pi
import random

# np.sin(...)能够接收一个ndarray，然后返回以ndarray中的元素为自变量的正弦函数的值，组成一个数组。
# 返回的数组的形状和传送的数组的形状一一对应。
a = np.arange(1, 16).reshape(3, 5)
b = np.sin(a)
print(b)
print(np.sin(pi/a))

# 相同形状的数组能够进行加减乘除运算，即在对应的位置上进行加减乘除。
a = np.arange(1, 5).reshape(2, 2)
b = np.arange(3, 7).reshape(2, 2)
print(f'a:\n{a}\n b:\n{b}\n')
print(f'a-b:\n{a - b}\n')
print(f'a+b:\n{a + b}\n')
print(f'a*b:\n{a * b}\n')
print(f'a/b:\n{a / b}\n')

# 两个数组之间数组也能进行矩阵相乘，使用 '@' 符号，前提是满足相乘的条件，否则会报错。
print(f'a@b:\n{a @ b}\n')
# 另一种表达矩阵相乘的写法: a.dot(b)
print(f'a@b:\n{a.dot(b)}\n')

# NumPy在大部分情况下能够自动进行类型转换，但在特定情况下不会进行类型转换。
# 比如从浮点数到整型的转换。
a = np.arange(1, 5, dtype=int).reshape(2, 2)
# np.random.default_rng()创造一个随机变量生成器。
rg = np.random.default_rng(1)
# rg.random()可以接收一个元组，用于创建什么形状的矩阵。
b = rg.random((2, 2), dtype=float)
try:
    a += b
except TypeError as e:
    print(e)

# NumPy还可以进行指数运算。
a = np.arange(1, 5, dtype=int).reshape(2, 2)
print(f'"a" before expotential arithmetic:\n{a}\n')
a = np.exp(a)
print(f'"a" after expotential arithmetic:\n{a}\n')

# NumPy可以分别用.min(), .max(), .sum()得到矩阵中最小、最大的数还有所有数值的和。
# .mean()求平均值，.var()求方差,.std()求标准差。
a = np.random.default_rng(1).random((2, 2))
print(a)
print(a.min(), a.max(), a.sum(), sep=', ')
print(a.mean(), a.var(), a.std(), sep=', ')

# .min(), .max(), .sum()还可以指定特定的轴。
print(a.min(axis=0))
print(a.max(axis=1))
print(a.sum(axis=1))

# NumPy可以用np.sqrt()计算数值的平方根。
a = np.array([1, 2, 3, 4]).reshape(2, 2)
print(np.sqrt(a))

# NumPy可以用numpy.abs()得到数组元素的绝对值。
a = np.array([random.uniform(-10, 10) for i in range(20)]).reshape((10, 2))
print(a)
a = np.abs(a)
print(a)

# NumPy可以用np.floor()向下取整，np.ceil()向上取整，np.round()进行四舍五入，np.trunc()截断小数点后的数字。
a = np.array([random.uniform(-10, 10) for i in range(20)]).reshape((10, 2))
print(a)
print(np.floor(a))
print(np.ceil(a))
print(np.round(a))
print(np.trunc(a))

# NumPy可以使用np.modf()将数组的小数部分和整数部分分开。
a = np.array([random.uniform(-10, 10) for i in range(20)]).reshape((10, 2))
print(a)
# np.modf()得到两个数组，可以用x, y分别接收。
x, y = np.modf(a)
print(x, y, sep='\n')

# nan, inf 是两个特殊的浮点数。nan表示Not_A_Number, inf表示INFinity。
print(float('nan'))
print(float('inf'))
a = np.arange(0, 4, dtype=float).reshape((2, 2))

try:
    print(0/a, 4/a, sep='\n ')
    # 用np.isnan()判断数组的元素是不是nan, 用np.isinf()判断数组的元素是不是inf。
    print(np.isnan(0/a))
    print(np.isinf(4/a))
except RuntimeWarning as e:
    print(e)

# np.maximum(a, b)接收两个形状相同的数组，返回一个对应位置上更大的那一个组成的数组。同理适用于np.minimum(a, b)。
a = np.array([random.randint(-10, 10) for i in range(20)]).reshape((10, 2))
b = np.array([random.randint(-10, 10) for i in range(20)]).reshape((10, 2))
print(np.maximum(a, b))
print(np.minimum(a, b))




