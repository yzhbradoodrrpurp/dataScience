# -*- coding = utf-8 -*-
# @Time: 2024/10/23 16:23
# @Author: Zhihang Yi
# @File: 015BackTrader.py
# @Software: PyCharm

import pandas as pd
import yfinance as yf
import backtrader as bt


class DoubleSMAStrategy(bt.Strategy):
    def __init__(self):
        # 在 '__init__()' 方法中定义你需要的指标。
        self.ma21 = bt.indicators.SimpleMovingAverage(self.data.close, period=21)
        self.ma55 = bt.indicators.SimpleMovingAverage(self.data.close, period=55)

    def next(self):
        # 在 'next()' 方法中规划你的策略逻辑。
        pass
        # 如果没有持仓，则进行买入操作。
        if not self.position:
            if True:
                if self.ma21 > self.ma55:
                    self.buy()
        elif self.ma21 < self.ma55:
            self.sell()


def main():
    # code = input('Enter the code: ')
    # start = input('Enter the start date: ')
    # end = input('Enter the end date: ')

    code = 'SOL-USD'
    start = '2024-6-3'
    end = '2024-10-22'

    stock = yf.download(code, start=start, end=end, interval='1h')
    stock = stock.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]

    # 用 'bt.Cerebro()' 创建一个回测环境并命名为 'cerebro' .
    cerebro = bt.Cerebro()
    # 将自己定义的类(策略) 'DoubleSMAStrategy' 通过 'cerebro.addstrategy(...)' 添加到回测环境中。
    cerebro.addstrategy(DoubleSMAStrategy)

    # 将从yfinance中得到的数据通过 'bt.feeds.PandasData(dataname=...)' 转换为PandasData对象。
    data = bt.feeds.PandasData(dataname=stock)
    # 将PandasData对象 'data' 通过 'cerebro.adddata(...)' 添加到回测环境中。
    cerebro.adddata(data)

    # initial_input = float(input('Enter your initial input: '))
    initial_input = 1000
    # 用 'cerebro.broker.setcash(...)' 设置起始金额，默认单位为USD。
    cerebro.broker.setcash(initial_input)

    # 运行回测环境。
    cerebro.run()
    # 回测结束后进行绘图。
    cerebro.plot()

    total_capital = cerebro.broker.getvalue()
    print(f'You have {total_capital:.2f} USD in total.')

    if total_capital > initial_input:
        profit = total_capital - initial_input
        return_ratio = profit / initial_input
        print(f'You\'ve earned {profit:.2f} USD from {code}.')
        print(f'The return ratio is {(return_ratio * 100):.2f}%.')
    else:
        loss = initial_input - total_capital
        loss_ratio = loss / initial_input
        print(f'You\'ve lost {loss:.2f} USD from {code}.')
        print(f'The loss ratio is {(loss_ratio * 100):.2f}%.')

    print(f'The whole process took you {(pd.to_datetime(end) - pd.to_datetime(start)).days} days.')


if __name__ == '__main__':
    main()
