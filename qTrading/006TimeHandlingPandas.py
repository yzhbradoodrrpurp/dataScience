# -*- coding = utf-8 -*-
# @Time: 2024/10/19 19:12
# @Author: Zhihang Yi
# @File: 006TimeHandlingPandas.py
# @Software: PyCharm

from datetime import datetime
import dateutil
import pandas as pd


# .strftime('...')是将一个datetime对象转化为字符串，
# .strptime('...')是将一个字符串转化为datetime对象。

now = datetime.now().strftime('%Y.%m.%d, %H:%M:%S')
print(now, type(now), sep='   ->   ')
now = datetime.strptime(now, '%Y.%m.%d, %H:%M:%S')
print(now, type(now), sep='   ->   ')

# pd.to_time('...')能够直接将str批量转换为datetime对象，不需要指定格式。
# 当传入的时间格式不同时，需要将format定义为'mixed'。
time1 = '2001-1-10, 19:23:40'
time2 = '2005.2.24, 2:34:49'
time3 = '2024/Oct/19 19:37:20'
time4 = '2022/12/11'
time = pd.to_datetime([time1, time2, time3, time4], format='mixed')
print(time)

# pd.date_range()能够批量生成时间(类型为datetime)，以每一天为间隔。
# 第一种做法是输入起始天和结束天。
time = pd.date_range('2022.11.10', '2022.12.14')
print(time)
# 第二种做法是输入起始天和天数，用periods控制
time = pd.date_range('2022.11.10', periods=35)
print(time)
# 第三种做法是不一定按天，也可以按小时，按周，按工作日等等，用freq控制。
# 'D': 天, 'W': 周, 'M': 月, 'YE': 年, 'B': 工作日, 'h': 小时, 'min': 分, 's': 秒。
time = pd.date_range('2022.11.10', periods=35, freq='B')
print(time)
