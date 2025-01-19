# -*- coding = utf-8 -*-
# @Time: 2024/10/16 18:34
# @Author: Zhihang Yi
# @File: 005copyOFndarray.py
# @Software: PyCharm

import numpy as np
from numpy import pi


# 对于ndarray之间的直接赋值，不会创造新的ndarray。
# 也就是说直接将a赋值给b，实际上a, b指的是同一个对象。
rg = np.random.default_rng(1)
a = rg.random((2, 3))
print(a)
b = a
b *= 2
print(a)

# 如果想要得到一份独立的ndarray复制品，那么需要用到.copy()
a = rg.random((2, 3))
print(a)
b = a.copy()
b *= 2
print(a)
print(b)

