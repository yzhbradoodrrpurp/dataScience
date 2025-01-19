# -*- coding = utf-8 -*-
# @Time: 2024/10/24 11:21
# @Author: Zhihang Yi
# @File: 016BackTraderWithStrategy.py
# @Software: PyCharm

import backtrader as bt
import yfinance as yf
import pandas as pd
import matplotlib.dates as mdates


class MAStrategy(bt.Strategy):
    def __init__(self):
        # BackTrader自带SMA均线，将 'self.data.close' 'period=21' 传入，表示用每天的收盘价绘制SMA21均线。
        self.sma21 = bt.indicators.SimpleMovingAverage(self.data.close, period=21)
        self.sma55 = bt.indicators.SimpleMovingAverage(self.data.close, period=55)

        # BackTrader自带MACD指标，'period_me1=13' 表示短线用EMA13，'period_me2=34' 表示长线用EMA34，'period_signal=9' 表示信号线用EMA9。
        self.macd = bt.indicators.MACD(self.data.close, period_me1=13, period_me2=34, period_signal=9)

        # 用于计算策略的胜率。
        self.total_trade = 0
        self.winning_trade = 0

        # 用于计算连续亏损的次数。
        self.continuous_loss_count = 0

    def next(self):
        # 'self.data' 就是传进来的股票数据，用 '.close[0]' 得到当前的收盘价。
        # 想要得到前一天的收盘价，就用 '.close[-1]' 获取。
        current_price = self.data.close[0]

        # 抄底策略：当一周跌幅大于35%时，买入。
        if (self.data.close[-7 * 24] - self.data.close[0]) / self.data.close[-7 * 24] > 0.35:
            # 每次交易的时候一定要判断是否持仓，否则会有bug出现。
            if not self.position:
                # 设置买入的份额，用 'self.broker.getcash()' 得到可用资金。
                self.buy(size=(self.broker.getcash() / current_price))

        # 如果有持仓且亏损超过总投入的3%并且三天连续下跌，则逃跑。
        if self.position:
            # 用 'self.prosition.price' 得到现在的持仓成本。
            if (self.position.price - current_price) / self.position.price >= 0.03 and self.data.close[-2] > self.data.close[-1] > self.data.close[0]:
                # 'self.close()' 表示份额全部清仓卖出。
                self.close()

        # 这个条件用于寻找MACD线斜率为0的点。
        if -0.03 < (self.macd.macd[0] - self.macd.macd[-1]) / self.macd.macd[0] < 0.03:
            # 斜率为0且MACD线小于信号线。
            if self.macd.macd[0] < self.macd.signal[0]:
                # 用于寻找SMA斜率为0的点，判断趋势的改变。
                if self.sma55[-2] < self.sma55[-1] < self.sma55[0]:
                    if not self.position:
                        # 当连续亏损次数小于3时才继续这个买入策略。
                        if self.continuous_loss_count < 3:
                            self.buy(size=(self.broker.getcash() / current_price))
                        else:
                            self.continuous_loss_count -= 1

        # 这个策略是基于SMA21和SMA55，表明趋势已经形成。
        if self.sma21[0] > self.sma55[0] > self.sma55[-1]:
            if not self.position:
                # 当连续亏损次数小于2时才继续这个买入策略。
                if self.continuous_loss_count < 2:
                    self.buy(size=(self.broker.getcash() / current_price))
                else:
                    self.continuous_loss_count -= 1

        # 这个条件用于寻找MACD线斜率为0的点。
        if -0.03 < (self.macd.macd[0] - self.macd.macd[-1]) / self.macd.macd[0] < 0.03:
            # 斜率为0且MACD线大于信号线。
            if self.macd.macd[0] > self.macd.signal[0]:
                if self.position:
                    self.close()

        # 趋势已经改变。
        if self.sma21[0] < self.sma55[0] and -0.03 < (self.sma55[0] - self.sma55[-1]) / self.sma55[-1] < 0.03:
            if self.position:
                self.close()

    # 'notify_trade()' 方法在每一次平仓的时候都会被调用。
    # 平仓：buy()之后sell() / sell()之后buy() / 调用close()。
    def notify_trade(self, trade):
        # 'trade' 变量是一个实例变量，包含了多种交易的信息。
        # '.isopen' '.isclosed' 判断交易是否处于活动状态或者平仓。
        # '.pnl' 表示一笔交易结束时的盈亏。
        if trade.isclosed:
            self.total_trade += 1
            # 这一笔的盈亏大于0，则胜单+1，连续亏损次数归零。
            if trade.pnl > 0:
                self.winning_trade += 1
                self.continuous_loss_count = 0
            # 这一笔的盈亏小于0，则连续亏损次数+1.
            elif trade.pnl < 0:
                self.continuous_loss_count += 1

    # 'stop()' 方法在所有的数据都被迭代完成后进行。
    def stop(self):
        print(f'The winning rate of your strategy is {(self.winning_trade * 100 / self.total_trade):.2f}%.')


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

    reports(code, initial_input, total_capital, duration, max_drawdown)


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


def reports(code, initial_input, total_capital, duration, max_drawdown):
    if total_capital > initial_input:
        profit = total_capital - initial_input
        print(f'Your total capital is {total_capital:.2f} USD right now.')
        print(f'You\'ve earned {profit:.2f} USD from {code}, which took you {duration} days.')
        print(f'The return ratio of investment is {((profit / initial_input) * 100):.2f}%.')
    elif total_capital < initial_input:
        loss = initial_input - total_capital
        print(f'Your total capital is {total_capital:.2f} USD right now.')
        print(f'You\'ve lost {loss:.2f} USD from {code}, which took you {duration} days.')
        print(f'The loss ratio of investment is {((loss / initial_input) * 100):.2f}%.')
    else:
        print(f'Your profits offset the costs.')

    print(f'The maximum drawdown is {max_drawdown:.2f}%.')


if __name__ == '__main__':
    main()
