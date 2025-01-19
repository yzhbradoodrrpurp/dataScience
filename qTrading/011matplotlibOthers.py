# -*- coding = utf-8 -*-
# @Time: 2024/10/21 10:41
# @Author: Zhihang Yi
# @File: 011matplotlibOthers.py
# @Software: PyCharm

from matplotlib import pyplot as plt
import numpy as np
import random


plt.figure()

plt.subplot(2, 1, 1)
x = ['Alice', 'Bob', 'Charlie']
y = np.array([random.uniform(4, 10) for i in range(3)])
# .bar()用于画柱状图，同样接受两个list/tuple/ndarray。
# 可以通过 'width' 设置柱的宽度，'color' 设置颜色。
plt.bar(x, y, width=0.2, color='grey')


plt.subplot(2, 1, 2)
# .pie()用于画饼图，只用接收一个list/tuple/ndarray，用于确定百分比(也就是说列表中的元素类型为int/float)。
# 'labels' 用于给每个百分比定义一个标签，'autopct' 用于显示百分比。
plt.pie(np.array([random.uniform(1, 10) for i in range(4)]), labels=['China', 'the USA', 'England', 'Japan'], autopct='%0.2f%%')

plt.tight_layout()
plt.show()

