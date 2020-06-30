import yfinance as yf
from yahoofinancials import YahooFinancials
import datetime
from pandas_datareader import data as pdr
import pandas as pd

way = 3
this = 'TTEK'
start='2020-01-01'
end=datetime.date.today()

def retrieve_yahoo_data(stock, start, end, method=1):
  """
  Function used to retrieve Yahoo Finance stock data
  """
  if method == 1:
    stock = yf.Ticker(stock)
    hist = stock.history(start=start, end=end, auto_adjust=False)
    prices = []
    for index, day in hist.iterrows():
      day_info = (index, day['Open'], day['High'], day['Low'], day['Close'], day['Volume'], day['Adj Close']) 
      prices.append(day_info)
  
  if method == 2:
    stock_2 = YahooFinancials(stock)
    stock_info = stock_2.get_historical_price_data(start, end.strftime('%Y-%m-%d'), 'daily')
    prices = []
    prices_ = stock_info[stock]['prices']
    for p in prices_:
      day_info = (pd.Timestamp(p['formatted_date']), round(p['open'], 2), round(p['high'], 2), round(p['low'], 2), round(p['close'], 2), p['volume'], round(p['adjclose'], 2))
      prices.append(day_info)
    return prices
  
  if method == 3:
    yf.pdr_override()
    data = pdr.get_data_yahoo([stock], start = start, end = end)
    prices = []
    for index, day in data.iterrows():
      day_info = (index, round(day['Open'], 2), round(day['High'], 2), round(day['Low'], 2), round(day['Close'], 2), day['Volume'], round(day['Adj Close'], 2))
      prices.append(day_info)
    return prices


#retrieve_yahoo_data(this, start, end, method=2)


