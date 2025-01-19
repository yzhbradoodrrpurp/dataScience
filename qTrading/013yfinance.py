# -*- coding = utf-8 -*-
# @Time: 2024/10/21 19:40
# @Author: Zhihang Yi
# @File: 013yfinance.py
# @Software: PyCharm

import yfinance as yf
import mplfinance as fin
"""
yfinance是一个完全免费、开源的量化数据工具。
详情请见yfinance的Github主页，或者作者的教程页: 'https://aroussi.com/post/python-yahoo-finance'
"""

microsoft = yf.download('MSFT', start='2022-10-10', end='2024-10-21')
microsoft = microsoft.iloc[:, [0, 1, 2, 3, 5]]

fin.plot(microsoft, type='candle', volume=True)
