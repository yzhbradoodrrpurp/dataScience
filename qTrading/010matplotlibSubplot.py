# -*- coding = utf-8 -*-
# @Time: 2024/10/21 09:54
# @Author: Zhihang Yi
# @File: 010matplotlibSubplot.py
# @Software: PyCharm

from matplotlib import pyplot as plt
import numpy as np


"""
在009matplotlib1.py中的画图方法不适用于在一个图形窗口中画出多个不同的图。
下面我们引入一种新的、更普适的方法。
"""

# 创建一个新的图形窗口。
plt.figure()

# 在这个图形窗口里加入一个图。
# 'plt.subplot(2， 1, 1)' 表示将窗口分为两行一列，占据第一个位置(上面的那个位置)。
plt.subplot(2, 1, 1)
plt.title('(x, y) Coordinates:')
plt.xlabel('x')
plt.ylabel('y')

x = np.linspace(-10, 10, 10000)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)

plt.plot(x, y1, color='red', label='y=sin(x)')
plt.plot(x, y2, color='blue', label='y=cos(x)')
plt.plot(x, y3, color='green', label='y=tan(x)')
plt.legend()

plt.xlim(-10, 10)
plt.ylim(-1, 1)
plt.xticks(np.arange(-10, 12, 2))
plt.yticks([-1, -np.sqrt(3)/2, -np.sqrt(2)/2, -1/2, 0, 1/2, np.sqrt(2)/2, np.sqrt(3)/2, 1])

# 'plt.subplot(2, 1, 2)' 创建了第二个子图，放在第二个位置上(下面那个位置)。
plt.subplot(2, 1, 2)
plt.title('(x, y) Coordinates:')
plt.xlabel('x')
plt.ylabel('y')

x = np.linspace(0, 20, 10000)
y1 = np.exp(x)
y2 = np.sqrt(x)
y3 = np.arctan(x)

plt.plot(x, y1, color='red', label='y=exp(x)')
plt.plot(x, y2, color='blue', label='y=sqrt(x)')
plt.plot(x, y3, color='green', label='y=arctan(x)')
plt.legend()

plt.xlim(0, 20)
plt.ylim(0, 20)
plt.xticks(np.arange(0, 22, 2))
plt.yticks(np.arange(0, 22, 2))

# 'plt.tight_layout()' 用于自动调整子图的间距，以使得图形在显示时不重叠。
plt.tight_layout()
plt.show()
