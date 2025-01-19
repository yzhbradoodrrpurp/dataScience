# -*- coding = utf-8 -*-
# @Time: 2024/10/20 20:12
# @Author: Zhihang Yi
# @File: 001DrawFunctions.py
# @Software: PyCharm

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


x = np.linspace(-20, 20, 10000)
y1 = x
y2 = np.pow(x, 2)
y3 = 2*np.pow(x, 3) + 5*np.pow(x, 2) + 2*x + 1

plt.plot(x, y1, color='blue', label='y=x')
plt.plot(x, y2, color='red', label='y=x²')
plt.plot(x, y3, color='green', label='2x³+5x²+2x+1')

plt.xlim(-20, 20)
plt.ylim(-20, 20)

plt.xlabel('x')
plt.ylabel('y')
plt.title('(x, y) Coordinates:')

plt.xticks(np.arange(-20, 20, 2))
plt.yticks(np.arange(-20, 20, 2))
plt.legend()

plt.show()
