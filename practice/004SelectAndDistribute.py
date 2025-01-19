# -*- coding = utf-8 -*-
# @Time: 2024/10/31 15:49
# @Author: Zhihang Yi
# @File: 004SelectAndDistribute.py
# @Software: PyCharm

from datetime import datetime

import numpy as np
import pandas as pd

import okx.MarketData
import okx.PublicData
import okx.TradingData


def main():
    MarketAPI, PublicAPI, TradingDataAPI = initialize_api()

    stocks = pick_stocks(MarketAPI, PublicAPI, TradingDataAPI)

    stock_priority = distribute_money(stocks, MarketAPI)
    print(stock_priority)


def initialize_api():
    api_key = 'f18f4e68-d997-4c8c-8d03-cc1a43f90cbc'
    api_secret_key = '505173C38B2FB4898FD22DFABE227E9E'
    passphrase = 'Yzh.1683491579'

    MarketAPI = okx.MarketData.MarketAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase)
    PublicAPI = okx.PublicData.PublicAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase)
    TradingDataAPI = okx.TradingData.TradingDataAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase)

    return MarketAPI, PublicAPI, TradingDataAPI


def pick_stocks(MarketAPI, PublicAPI, TradingDataAPI):
    stock_pool = [
        'BTC-USDT', 'ETH-USDT', 'BNB-USDT', 'SOL-USDT', 'TRX-USDT',
        'SHIB-USDT', 'LTC-USDT', 'DOGE-USDT', 'XRP-USDT', 'BCH-USDT',
        'SUI-USDT', 'ADA-USDT', 'PEPE-USDT', 'BOME-USDT'
    ]

    stock_pool = public_factors(stock_pool, PublicAPI)
    stock_pool = trading_data_factors(stock_pool, TradingDataAPI)

    return stock_pool


def public_factors(stock_pool, PublicAPI):
    funding_rates = []
    next_funding_rates = []
    premiums = []

    for stock in stock_pool:
        try:
            stock_info = PublicAPI.get_funding_rate(instId=stock + '-SWAP')
        except Exception:
            return []
        else:
            funding_rate = float(stock_info['data'][0]['fundingRate'])
            next_funding_rate = float(stock_info['data'][0]['maxFundingRate'])
            premium = float(stock_info['data'][0]['premium'])

        funding_rates.append(funding_rate)
        next_funding_rates.append(next_funding_rate)
        premiums.append(premium)

    funding_rates = pd.Series(funding_rates, index=stock_pool)
    funding_rates = standarize(funding_rates)

    next_funding_rates = pd.Series(next_funding_rates, index=stock_pool)
    next_funding_rates = standarize(next_funding_rates)

    premiums = pd.Series(premiums, index=stock_pool)
    premiums = standarize(premiums)

    stock_info = pd.DataFrame({
        'funding_rate': funding_rates,
        'next_funding_rate': next_funding_rates,
        'premium': premiums
    })

    indicators = stock_info.iloc[:, 1] - stock_info.iloc[:, 0] + stock_info.iloc[:, 2]

    stock_pool = []

    for i in range(7):
        max_value = indicators.max()
        prospective = indicators[indicators == max_value].index[0]
        indicators.drop(prospective, inplace=True)
        stock_pool.append(prospective)

    return stock_pool


def standarize(series):
    series = (series - series.mean()) / series.std()
    return series


def trading_data_factors(stock_pool, TradingDataAPI):
    stock_pool = margin_lending_ratio_factor(stock_pool, TradingDataAPI)
    stock_pool = taker_factor(stock_pool, TradingDataAPI)

    return stock_pool


def margin_lending_ratio_factor(stock_pool, TradingDataAPI):
    average_ratios = []

    for stock in stock_pool:
        stock = stock.split('-')[0]
        try:
            stock_info = TradingDataAPI.get_margin_lending_ratio(ccy=stock)
        except Exception:
            return []
        else:
            ratios = [float(stock_info['data'][i][1]) for i in range(24)]
            average_ratio = pd.Series(ratios).mean()
            average_ratios.append(average_ratio)

    average_ratios = pd.Series(average_ratios, index=stock_pool)
    average_ratios = standarize(average_ratios)

    stock_pool = []

    for i in range(5):
        max_value = average_ratios.max()
        prospective = average_ratios[average_ratios == max_value].index[0]
        average_ratios.drop(prospective, inplace=True)
        stock_pool.append(prospective)

    return stock_pool


def taker_factor(stock_pool, TradingDataAPI):
    buy_ins = []

    for stock in stock_pool:
        stock = stock.split('-')[0]
        try:
            stock_info = TradingDataAPI.get_taker_volume(ccy=stock, instType='SPOT')
        except Exception:
            return []
        else:
            buy_vol = float(stock_info['data'][0][2])
            sell_vol = float(stock_info['data'][0][1])
            buy_in = buy_vol - sell_vol
            buy_ins.append(buy_in)

    buy_ins = pd.Series(buy_ins, index=stock_pool)
    buy_ins = standarize(buy_ins)

    stock_pool = []

    for i in range(3):
        max_value = buy_ins.max()
        prospective = buy_ins[buy_ins == max_value].index[0]
        buy_ins.drop(prospective, inplace=True)
        stock_pool.append(prospective)

    return stock_pool


def distribute_money(stocks, MarketAPI):
    total_cash = 1000
    average_closes = []
    today_closes = []

    for stock in stocks:
        try:
            stock_info = MarketAPI.get_candlesticks(instId=stock)
        except Exception:
            return pd.Series()
        else:
            closes = [float(stock_info['data'][i][4]) for i in range(21)]
            average_close = pd.Series(closes).mean()
            today_close = closes[0]
            average_closes.append(average_close)
            today_closes.append(today_close)

    today_closes = pd.Series(today_closes, index=stocks)
    average_closes = pd.Series(average_closes, index=stocks)

    today_closes = standarize(today_closes)
    average_closes = standarize(average_closes)

    closes = pd.DataFrame({'today_close': today_closes, 'average_close': average_closes}, index=stocks)
    factors = closes.loc[:, 'average_close'] - closes.loc[:, 'today_close'] / closes.loc[:, 'average_close']

    stock_priority = []

    for i in range(len(stocks)):
        max_value = factors.max()
        prospective = factors[factors == max_value].index[0]
        factors.drop(prospective, inplace=True)
        stock_priority.append(prospective)

    stock_priority = pd.Series([total_cash * (1/2), total_cash * (1/3), total_cash * (1/6)], index=stock_priority)

    return stock_priority


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('Keyboard Interrupt.')
