# -*- coding = utf-8 -*-
# @Time: 2024/10/22 16:44
# @Author: Zhihang Yi
# @File: 014DoubleMAStrategy.py
# @Software: PyCharm

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import mplfinance as fin

import yfinance as yf


def main():
    code = input('Enter the stock code: ')
    start = input('Enter the start date: ')
    end = input('Enter the end date: ')
    
    while True:
        try:
            stock = yf.download(code, start=start, end=end, interval='1h')
        except Exception as e:
            print(e)

        if stock.empty is False:
            break
        else:
            print('The information is blank. We\'ll initiate a request again.')

    # 在得到了stock的每日股价之后，用 'rolling(window=...)' 得到这一时刻与之前20时刻、49时刻的收盘股价平均值。
    ma_21 = stock.loc[:, 'Close'].rolling(window=20).mean()
    ma_55 = stock.loc[:, 'Close'].rolling(window=54).mean()

    plot_candlesticks(code, stock, ma_21, ma_55)
    trade_days = store_buy_sell_day(ma_21, ma_55)
    buy_and_sell(code, stock, trade_days)


def plot_candlesticks(code, stock, ma_21, ma_55):
    # 'make_addplot()' 用于在金融图表中添加额外的图形。
    # 第一个数值接收一个Series或者一维DataFrame(以datetime为索引)。
    # 'panel=0' 表示和k线图画在同一个图中。MACD的图就可以设置为 'panel=1' 。
    plot1 = fin.make_addplot(ma_21, panel=0, color='red', linestyle='--', title='MA21')
    plot2 = fin.make_addplot(ma_55, panel=0, color='orange', linestyle='--', title='MA55')
    # 组成一个列表，然后传给 'fin.plot()' 中的 'addplot' 参数。
    addplot = [plot1, plot2]

    fin.plot(stock, type='candle', volume=False, title=f'{code} Share Price', xlabel='Date', ylabel='USD', addplot=addplot)


def store_buy_sell_day(ma_21, ma_55):
    whether_to_hold = (ma_21 > ma_55)
    # diff()方法是一个pandas中Series, DataFrame专属的方法，用于判断当前位置的元素和前一个位置的元素是否相同。
    # 类型为int, float时会返回差值；为其它时返回0(相同)/1(不相同)。
    # 值得注意的是，第一个数值是NaN，因为不存在前一个元素。
    trade_days = whether_to_hold[whether_to_hold.diff() == 1]
    buy_days = trade_days[trade_days]
    sell_days = trade_days[not trade_days]

    buy_days.to_csv('014buy_days.csv')
    sell_days.to_csv('014sell_days.csv')

    return trade_days


def buy_and_sell(code, stock, trade_days):
    # 起始资金为1000美元。
    capital = 1000
    first_trade_day = 0

    while ~trade_days.iloc[first_trade_day]:
        first_trade_day += 1
    else:
        trade_days = trade_days.iloc[first_trade_day:]

    for day in trade_days.index:
        if trade_days.loc[day]:
            shares = capital / stock.loc[day, 'Close']
        else:
            capital = shares * stock.loc[day, 'Close']

    print(f'The total capital you have is {capital:.2f} USD.')

    if capital > 1000:
        print(f'You\'ve earned {(capital - 1000):.2f} USD from {code}.')
        print(f'The ratio of investment return is {((capital - 1000) * 100 / 1000 ):.2f}%.')
    elif capital < 1000:
        print(f'You\'ve lost {(1000-capital):.2f} USD.')
        print(f'You\'ve lost {((1000 - capital) * 100 / 1000):.2f}% of your money.')
    else:
        print(f'Your earnings and costs are equal.')


if __name__ == '__main__':
    main()
