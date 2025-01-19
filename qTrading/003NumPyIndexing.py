# -*- coding = utf-8 -*-
# @Time: 2024/10/15 19:11
# @Author: Zhihang Yi
# @File: 004numPyIndexingAndIterating.py
# @Software: PyCharm

import numpy as np
from numpy import pi
import random


# ndarray的引用和Python中的列表被引用是一模一样的。
a = np.arange(0, 10)**3
print(a)
print(a[2:4])
print(a[2::3])
print(a[::2])
print(a[::-1])

# NumPy甚至可以接收一个函数来创建一个数组。
def f(x, y):
    return x * 20 + y


# 创建一个4*5的数组，并且x取值[0, 4), y取值[0, 5)
a = np.fromfunction(f, (4, 5), dtype=int)
print(a)
# 索引和切片的方式其实和一维的类似。
print(a[0])
print(a[1, 2])
print(a[:, 2])
print(a[::2, 3])
print(a[::2, ::2])

"""
The dots (...) represent as many colons as needed to produce a complete indexing tuple. 
For example, if x is an array with 5 axes, then:

x[1, 2, ...] is equivalent to x[1, 2, :, :, :],
x[..., 3] to x[:, :, :, :, 3] and
x[4, ..., 5, :] to x[4, :, :, 5, :].
"""

# .flat是一个属性，表示数组以一维的形式存在的遍历器，便于一次遍历，而不用写多重循环。
rg = np.random.default_rng(1)
a = rg.random((2, 3, 5, 2, 6, 8))
print(a.flat)
for item in a.flat:
    print(item)

# .ravel()是一个方法，能够返回多维数组压缩成一维数组的。
flattened_a = a.ravel()
print(flattened_a)

# .T也是一个属性，表示这个矩阵(数组)的转置矩阵。
a = np.arange(0, 10).reshape(2, 5)
print(a)
print(a.T)

# .resize()和.reshape()的区别：
"""
.reshape()不会更改原来的矩阵，并且返回一个新的矩阵。
除此之外，.reshape()要求矩阵中元素的个数不能改变。

.resize()直接更改原来的矩阵，不会返回一个新矩阵。
除此之外，.resize()能够改变原来矩阵元素的个数。
如果变多，那么多出来的元素会按照C-Style用0来填满。
如果变少，则按照C-Style去掉末尾的几个元素。

另外，.reshape(x, y), .resize((x, y))
"""

# 矩阵可以用.vstack((x, y))进行垂直组合，.hstack((x, y))进行水平组合。
rg = np.random.default_rng(1)
a = rg.random((2, 3))
rg = np.random.default_rng(2)
b = rg.random((2, 3))
print(f'a:\n{a}\nb:\n{b}\n')
print(f'a,b stacked vertically:\n{np.vstack([a, b])}')
print(f'a,b stacked horizontally:\n{np.hstack([a, b])}')

# 布尔索引。
a = np.array([random.randint(1, 21) for i in range(30)]).reshape(10, 3)
print(a)
a = a[a > 5]
print(a)
a = a[(a < 15) & (a % 2 == 0)]
print(a)
a = a[(a < 10) | (a % 3 == 0)]
print(a)

# 花式索引。
a = np.array([random.randint(10, 51) for i in range(20)])
print(a)
a = a[[1, 3, 6, 9, 19]]
print(a)



