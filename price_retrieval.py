import datetime
import warnings
import MySQLdb as mdb
import requests
import yfinance as yf
from yahoofinancials import YahooFinancials
from pandas_datareader import data as pdr


# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
  """
  Obtains a list of the ticker symbols in the database
  """
  cur = con.cursor()
  cur.execute("SELECT id, ticker FROM symbol")
  data = cur.fetchall()
  return [(d[0], d[1]) for d in data]


def get_daily_historic_data_yahoo(ticker, start_date='2020-01-01', end_date='2020-02-01'):
  """
  Obtains data from Yahoo Finance and returns a list of tuples
 
  ticker: Yahoo Finance ticker symbol
  start_date: Start date in YYYY-MM-DD format or datetime
  end_date: End date in YYYY-MM-DD format or datetime
  """

  # Use yfinance to access all stock data and get it ready to store
  start = datetime.datetime(2019, 1, 1)
  end = datetime.datetime.today()
  yf.pdr_override()
  data = pdr.get_data_yahoo([ticker], start=start, end=end)
  prices = []
  for index, day in data.iterrows():
    day_info = (index, day['Open'], day['High'], day['Low'], day['Close'], day['Volume'], day['Adj Close'])
    print(day_info)
    prices.append(day_info)
  return prices




if __name__ == "__main__":
  # This ignores warnings regarding Data Truncation from the Yahoo precision to Decimal (19,4) datatypes
  warnings.filterwarnings('ignore')
  
  # Loop over the tickers and insert the daily historical data into the db 
  tickers = obtain_list_of_db_tickers()
  lentickers = len(tickers)
  for i, t in enumerate(tickers):
    if i < 23: continue
    stock_tk = t[1]
    if '.' in stock_tk: stock_tk = stock_tk.replace('.', '-')
    print("Adding data for %s: %s out of %s" % (stock_tk, i+1, lentickers))
    yf_data = get_daily_historic_data_yahoo(stock_tk)
