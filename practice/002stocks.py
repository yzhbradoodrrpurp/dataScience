# -*- coding = utf-8 -*-
# @Time: 2024/10/22 10:00
# @Author: Zhihang Yi
# @File: 002stocks.py
# @Software: PyCharm

import mplfinance as fin
import yfinance as yf
import pandas as pd


def main():
    microsoft = yf.download('MSFT', start='2022-10-01', end='2024-10-20')
    apple = yf.download('AAPL', start='2022-10-01', end='2024-10-20')
    nvidia = yf.download('NVDA', start='2022-10-01', end='2024-10-20')

    microsoft.to_csv('MSFT.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    apple.to_csv('AAPL.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    nvidia.to_csv('NVDA.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    fin.plot(microsoft, type='candle', volume=True)
    fin.plot(apple, type='candle', volume=True)
    fin.plot(nvidia, type='candle', volume=True)

    bool1 = (microsoft.loc[:, 'Close'] - microsoft.loc[:, 'Open']) / microsoft.loc[:, 'Open'] > 0.03
    microsoft_bull = microsoft.loc[bool1, :]
    microsoft_bull.to_csv('MSFT_bull.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    bool2 = (apple.loc[:, 'Close'] - apple.loc[:, 'Open']) / apple.loc[:, 'Open'] > 0.03
    apple_bull = apple.loc[bool2, :]
    apple_bull.to_csv('APPL_bull.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    bool3 = (nvidia.loc[:, 'Close'] - nvidia.loc[:, 'Open']) / nvidia.loc[:, 'Open'] > 0.03
    nvidia_bull = nvidia.loc[bool3, :]
    nvidia_bull.to_csv('NVDA-bull.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    bool1 = (microsoft.loc[:, 'Open'] - microsoft.loc[:, 'Close']) / microsoft.loc[:, 'Open'] > 0.02
    microsoft_bear = microsoft.loc[bool1, :]
    microsoft_bear.to_csv('MSFT-bear.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    bool2 = (apple.loc[:, 'Open'] - apple.loc[:, 'Close']) / apple.loc[:, 'Open'] > 0.02
    apple_bear = apple.loc[bool2, :]
    apple_bear.to_csv('APPL_bear.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    bool3 = (nvidia.loc[:, 'Open'] - nvidia.loc[:, 'Close']) / nvidia.loc[:, 'Open'] > 0.02
    nvidia_bear = nvidia.loc[bool3, :]
    nvidia_bear.to_csv('NVDA_bear.csv', columns=['Open', 'High', 'Low', 'Close', 'Volume'])


if __name__ == '__main__':
    main()
