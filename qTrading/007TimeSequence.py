# -*- coding = utf-8 -*-
# @Time: 2024/10/19 20:01
# @Author: Zhihang Yi
# @File: 007TimeSequence.py
# @Software: PyCharm

import pandas as pd
import random
import numpy as np


# 可以将时间作为Series的索引，然后根据年、月、日，高灵活度地进行检索。
# 要求索引是pandas中的datetime类型。
time = pd.date_range('2022-11-12', periods=100)
a = pd.Series(np.arange(100), index=time)
print(a)
print(a['2022'])
print(a['2022-11'])
print(a['2022-11-20'])
print(a['2022-11-22':'2022-12-06'])

# .resample()方法是一个只针对于以时间(datetime类型)为索引的Series或者DataFrame对象的方法。
# 它能够对Series或者DataFrame按照某种时间频率进行重采样。
print(a.resample('B').mean())
