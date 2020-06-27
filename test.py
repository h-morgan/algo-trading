import yfinance as yf
from yahoofinancials import YahooFinancials
import json
import datetime
from pandas_datareader import data as pdr

way = 3
this = 'TTEK'

if way == 1:
  stock = yf.Ticker(this)
  hist = stock.history(period="max")
  print(hist.head())


if way == 2:

  st = this

  stock_2 = YahooFinancials(st)
  stock_info = stock_2.get_historical_price_data('2010-01-01', '2010-01-10', 'daily')

  prices = stock_info[st]['prices']
  print(prices)

  for p in prices:
    print(p['formatted_date'], p['open'], p['high'], p['low'], p['close'])


if way == 3:
  start = datetime.datetime(2019, 1, 1)
  end = datetime.datetime.today()

  yf.pdr_override()
  data = pdr.get_data_yahoo([this], start = start, end = end)
  print(data.head())
