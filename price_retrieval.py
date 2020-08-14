import datetime
import warnings
import MySQLdb as mdb
import requests
import yfinance as yf
from yahoofinancials import YahooFinancials
from pandas_datareader import data as pdr
import utils


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


def get_daily_historic_data_yahoo(ticker, start_date='2010-01-01', end_date=datetime.date.today()):
  """
  Obtains data from Yahoo Finance and returns a list of tuples
 
  ticker: Yahoo Finance ticker symbol
  start_date: Start date in YYYY-MM-DD format or datetime
  end_date: End date in YYYY-MM-DD format or datetime
  """

  # Use yfinance to access all stock data and get it ready to store
  try:
    prices = utils.retrieve_yahoo_data(ticker, start_date, end_date, method=2)
    return prices
  except:
    prices = utils.retrieve_yahoo_data(ticker, start_date, end_date, method=1)
    return prices
  

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
  """
  Takes a list of tuples of daily data and adds it to the MySQL database
  Appends the vendor ID and symbol ID to the data

  daily_data: List of tuples of the OHLC data (with adj_close and volume)
  """
  # Create the time now
  now = datetime.datetime.utcnow()
  
  # Amend the data to include the vendor ID and symbole id
  daily_data = [(data_vendor_id, symbol_id, d[0], now, now, d[1], d[2], d[3], d[4], d[5], d[6]) for d in daily_data]
  
  # Create the insert strings
  column_str = "data_vendor_id, symbol_id, price_date, created_date, last_updated_date, open_price, high_price, low_price, close_price, volume, adj_close_price"
  insert_str = ("%s, " * 11)[:-2]
  final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)

  # Using the MySQL connection, carry out INSERT INTO for every symbol 
  cur = con.cursor()
  cur.executemany(final_str, daily_data)
  con.commit()


if __name__ == "__main__":
  # This ignores warnings regarding Data Truncation from the Yahoo precision to Decimal (19,4) datatypes
  warnings.filterwarnings('ignore')
  
  # Loop over the tickers and insert the daily historical data into the db 
  tickers = obtain_list_of_db_tickers()
  lentickers = len(tickers)
  for i, t in enumerate(tickers):
    stock_tk = t[1]
    if '.' in stock_tk: stock_tk = stock_tk.replace('.', '-')
    print("Adding data for %s: %s out of %s" % (stock_tk, i+1, lentickers))
    yf_data = get_daily_historic_data_yahoo(stock_tk) 
    insert_daily_data_into_db('1', t[0], yf_data)
  print("Successfully added Yahoo Finance pricing data to DB")

