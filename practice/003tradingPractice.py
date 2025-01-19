# -*- coding = utf-8 -*-
# @Time: 2024/10/22 10:52
# @Author: Zhihang Yi
# @File: 003tradingPractice.py
# @Software: PyCharm

import yfinance as yf
import pandas as pd


def main():
    microsoft = yf.download('MSFT', start='2010-01-01', end='2024-10-20')

    # resample()是一个以pandas中的datetime为索引的，只有Series, DataFrame能使用的方法。
    buy_days = microsoft.loc[:, 'Open'].resample('BMS').first()
    sell_days = microsoft.loc[:, 'Close'].resample('BYE').first()

    # 这是2010～2023已经收回的收益。
    costs = buy_days.sum() - buy_days.loc['2024'].sum()
    earnings = 12 * (sell_days.sum() - sell_days.loc['2024'].sum())
    interests = earnings - costs

    # 这是2024还持有的股票，在2024-10-18这一天的价值。
    holdings = len(buy_days.loc['2024']) * microsoft.loc['2024-10-18', 'Close']

    total = interests + holdings - buy_days.loc['2024'].sum()

    if total < 0:
        print(f'The loss of your money is {-total:.2f} USD.')
    else:
        print(f'The total interests you\' earned is {total:.2f} USD.')


if __name__ == '__main__':
    main()
