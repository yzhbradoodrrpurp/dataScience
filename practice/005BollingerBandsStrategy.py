# -*- coding = utf-8 -*-
# @Time: 2024/11/3 14:49
# @Author: Zhihang Yi
# @File: 005BollingerBandsStrategy.py
# @Software: PyCharm

import numpy as np
import pandas as pd

import backtrader as bt
import yfinance as yf


class Bollingerbands(bt.Strategy):
    def __init__(self):
        pass

    def next(self):
        pass

    def notify_trade(self, trade):
        pass

def main():
    code = 'SOL-USD'
    start = '2024-6-3'
    end = '2024-10-31'
    initial_input = 1000

    try:
        stock = yf.download(code, start=start, end=end, interval='1h')
    except Exception as e:
        print(e)

    stock = stock.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]

    total_capital, duration, max_drawdown = backtest(stock, initial_input)


def backtest(stock, initial_input):
    # 用 'bt.Cerebro()' 创建一个回测环境并命名为 'cerebro' 。
    cerebro = bt.Cerebro()
    # 用 'bt.addstrategy(...)' 添加创建的策略(类名 'Strategy' )。
    cerebro.addstrategy(MAStrategy)

    # 将下载下来的的pandas DataFrame数据通过 'bt.feeds.PandasData(dataname=...)' 转换得到BackTrader类数据。
    stock_data = bt.feeds.PandasData(dataname=stock)
    # 将BackTrader类数据通过 'cerebro.adddata(...)' 添加到回测环境中。
    cerebro.adddata(stock_data)

    # 通过 'cerebro.addanalyzer(...)' 为回测环境添加分析器，通过 'bt.analyzers.DrawDown' 添加回测分析。
    # '_name='DrawDown'' 表示后面会用DrawDown引用这个回测分析。
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')

    # 通过 'cerebro.broker.setcash(...)' 设置初始金额。
    cerebro.broker.setcash(initial_input)

    # 回测环境运行后，会返回多个策略的结果，组成一个列表。
    results = cerebro.run()
    cerebro.plot()

    # 用访问列表的方法得到第一个定义的策略数据。
    ma_result = results[0]
    # 用 'analyzers' 得到第一个策略运行结果的数据分析器，再用 'DrawDown(通过 _name= 自定义的名字) .get_analysis()' 得到这一个数据分析。
    drawdown_info = ma_result.analyzers.DrawDown.get_analysis()
    max_drawdown = drawdown_info['max']['drawdown']

    # 通过 'cerebro.broker.getvalue()' 得到最终的总资本。
    total_capital = cerebro.broker.getvalue()
    # 计算从最开始到现在的天数。
    start = stock.index[0]
    end = stock.index[-1]
    duration = (pd.to_datetime(end) - pd.to_datetime(start)).days

    return total_capital, duration, max_drawdown


if __name__ == '__main__':
    main()

