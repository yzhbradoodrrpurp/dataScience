# -*- coding = utf-8 -*-
# @Time: 2024/10/25 19:44
# @Author: Zhihang Yi
# @File: 017OKX.py
# @Software: PyCharm

# 这个模块用于调取okx交易所上的市场数据。
import okx.MarketData
import okx.PublicData
import okx.Account

import json
from datetime import datetime
import pandas as pd


def main():
    # 所有的数据申请都必须通过API得到。
    MarketAPI, PublicAPI, AccountAPI = initialize_api()

    stock = pick_stock(MarketAPI, PublicAPI)

    # 用 '.get_candlesticks(instId=..., bar='...')' 从API获得...(股票)的'...'级别K线图。
    # '.get_candlesticks(instId=..., bar='...')'返回的是一个字典，我们只需要 'data' 中的数据。
    candlesticks = MarketAPI.get_candlesticks(instId=stock, bar='1H')['data']
    close_price, sma21, sma55, macd, signal = get_indicators(candlesticks)

    begin_trade(close_price, sma21, sma55, macd, signal)


def initialize_api():
    api_key = '...'
    api_secret_key = '...'
    passphrase = '...'

    # 'okx.MarketData.MarketAPI(...)' 接收API的相关信息，然后创建一个可以获取市场数据的API。
    MarketAPI = okx.MarketData.MarketAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase)
    # 'okx.PublicData.PublicAPI(...)' 同样接收API的相关信息，然后创建一个可以获取公共数据的API。
    PublicAPI = okx.PublicData.PublicAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase)
    # 'okx.Account.AccountAPI(...)' 同样接收API的相关信息，然后创建一个可以控制个人账户的API。
    AccountAPI = okx.Account.AccountAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase)

    return MarketAPI, PublicAPI, AccountAPI


def pick_stock(MarketAPI, PublicAPI):
    # 这是我关注的股票池，我会从这里面选出看涨期望最高的股票。
    stock_pool = ['BTC-USDT', 'ETH-USDT', 'BNB-USDT', 'SOL-USDT', 'TRX-USDT']
    funding_rates = []
    next_funding_rates = []
    premiums = []

    for stock in stock_pool:
        # 用 'PublicAPI.get_funding_rate(...)' 得到某个品种永续合约的资金费率和溢价(合约的中间价和指数价格的差异)。
        # 当 'next_funding_rate' 大于 'funding_rate' 时，看涨期望较大。溢价为正时，看涨期望较大。
        stock_info2 = PublicAPI.get_funding_rate(instId=stock + '-SWAP')
        funding_rate = float(stock_info2['data'][0]['fundingRate'])
        next_funding_rate = (1 / 2) * (float(stock_info2['data'][0]['maxFundingRate']) + float(stock_info2['data'][0]['maxFundingRate']))
        premium = float(stock_info2['data'][0]['premium'])

        funding_rates.append(funding_rate)
        next_funding_rates.append(next_funding_rate)
        premiums.append(premium)

    funding_rates = pd.Series(funding_rates, index=stock_pool)
    funding_rates = (funding_rates - funding_rates.min()) / (funding_rates.max() - funding_rates.min())

    next_funding_rates = pd.Series(next_funding_rates, index=stock_pool)
    next_funding_rates = (next_funding_rates - next_funding_rates.min()) / (next_funding_rates.max() - next_funding_rates.min())

    premiums = pd.Series(premiums, index=stock_pool)
    premiums = (premiums - premiums.min()) / (premiums.max() - premiums.min())

    expectations = []

    for stock in stock_pool:
        expectation = next_funding_rates.loc[stock] - funding_rates.loc[stock] + premiums.loc[stock]
        expectations.append(expectation)
        print(stock, expectation)

    # 将list类型的 'expectations' 转换为pd.Series类型的数据，便于找出期望的最大值。
    expectations = pd.Series(expectations, index=stock_pool)
    prospective_stock = expectations[expectations == expectations.max()].index[0]
    print(f'The most prospective stock right now is {prospective_stock} whose expectation is {expectations[prospective_stock]}.')

    return prospective_stock


def get_close_price(candlesticks):
    close_price = []
    times = []

    for candlestick in candlesticks:
        close_price.append(float(candlestick[4]))
        # 'candlestick[0]' 得到的是毫秒级别的Unix时间戳，需要转换为秒级别的然后用 'datetime.fromtimestamp()' 转换为正常时间。
        time = datetime.fromtimestamp(float(candlestick[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        times.append(time)

    # 将close_price倒置，便于后面计算SMA，EMA。
    close_price = pd.Series(close_price, index=times).iloc[::-1]

    return close_price


def get_indicators(candlesticks):
    close_price = get_close_price(candlesticks)

    sma21, sma55 = get_sma(close_price)
    macd, signal = get_macd(close_price)

    return close_price, sma21, sma55, macd, signal


def get_sma(close_price):
    # 通过倒置后的close_price计算出SMA，然后将SMA倒置回来。最后我们统一规定长度为48.
    sma21 = close_price.rolling(window=21).mean().iloc[::-1].iloc[:48 + 1]
    sma55 = close_price.rolling(window=55).mean().iloc[::-1].iloc[:48 + 1]
    return sma21, sma55


def get_macd(close_price):
    ema13 = []
    ema34 = []

    # ema13_iterator, ema34_iterator分别是60+1个时刻之前的SMA13，SMA34的值。
    ema13_iterator = close_price.rolling(window=13).mean().iloc[::-1].iloc[60]
    ema34_iterator = close_price.rolling(window=34).mean().iloc[::-1].iloc[60]

    for i in range(60):
        ema13_iterator = (2 / (13 + 1)) * (close_price.iloc[::-1].iloc[60 - 1 - i] - ema13_iterator) + ema13_iterator
        ema13.append(ema13_iterator)

        ema34_iterator = (2 / (34 + 1)) * (close_price.iloc[::-1].iloc[60 - 1 - i] - ema34_iterator) + ema34_iterator
        ema34.append(ema34_iterator)

    ema13 = pd.Series(ema13, index=close_price.index[-60:]).iloc[::-1]
    ema34 = pd.Series(ema34, index=close_price.index[-60:]).iloc[::-1]

    macd = ema13 - ema34

    macd_iterator = macd.iloc[::-1].rolling(window=9).mean().iloc[::-1].iloc[48]
    signal = []

    for i in range(48):
        macd_iterator = (2 / (9 + 1)) * (macd.iloc[48 - 1 - i] - macd_iterator) + macd_iterator
        signal.append(macd_iterator)

    # 统一规定，所有的指标时间范围为48小时。
    signal = pd.Series(signal, index=close_price.index[-48:]).iloc[::-1]
    macd = macd.iloc[:48]

    return macd, signal


def begin_trade(close_price, sma21, sma55, macd, signal):
    initial_input = 1000

    # if -0.03 < (self.macd.macd[0] - self.macd.macd[-1]) / self.macd.macd[0] < 0.03:
    #     # 斜率为0且MACD线小于信号线。
    #     if self.macd.macd[0] < self.macd.signal[0]:
    #         # 用于寻找SMA斜率为0的点，判断趋势的改变。
    #         if self.sma55[-2] < self.sma55[-1] < self.sma55[0]:
    #             if not self.position:
    #                 # 当连续亏损次数小于3时才继续这个买入策略。
    #                 if self.continuous_loss_count < 3:
    #                     self.buy(size=(self.broker.getcash() / current_price))
    #                 else:
    #                     self.continuous_loss_count -= 1

    if -0.03 < (macd.iloc[0] - macd.iloc[1]) / macd.iloc[0] < 0.03:
        if macd.iloc[0] < signal.iloc[0]:
            if sma55[2] < sma55[1] < sma55[0]:
                pass


if __name__ == '__main__':
    main()
