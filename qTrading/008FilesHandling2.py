# -*- coding = utf-8 -*-
# @Time: 2024/10/20 15:25
# @Author: Zhihang Yi
# @File: 008FilesHandling2.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import random


# .to_csv()中也有几个特定的参数需要学习。
x = np.array([random.randint(-10, 10) for i in range(20)])
y = np.array([random.randint(-10, 10) for i in range(20)])
a = pd.DataFrame({'x': x, 'y': y})

# 'header' 接收一个bool类型变量，表明是否传入标题；'index' 同样接收一个bool类型变量，表示是否传入索引。
# 'header' 'index' 默认为True。
a.to_csv('008test', header=False, index=False)

# 'columns' 接收一个列表，表示将特定的列(列数/列名)传入.csv文件中。
a.to_csv('008test1.csv', columns=['x'])
