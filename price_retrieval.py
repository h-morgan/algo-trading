import datetime
import warnings
import MySQLdb as mdb
import requests


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

def get_daily_historic_data_yahoo(ticker, start_date=(2000,1,1), end_date=datetime.date.today().timetuple()[0:3]):
  """
  Obtains data from Yahoo Finance and returns a list of tuples
 
  ticker: Yahoo Finance ticker symbol
  start_date: Start date in (YYYY, M, D) fromat
  end_date: End date in (YYYY, M, D) format
  """
  # Construct the Yahoo URL with the correct integer query parameters for start/end dates
  # Note that some parameters are zero-based
  ticker_tup = (ticker, start_date[1]-1, start_date[2], start_date[0], end_date[1]-1, end_date[2], end_date[0])
  
  yahoo_url = "http://ichart.finance.yahoo.com/table.csv"
  yahoo_url += "?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"
  yahoo_url = yahoo_url % ticker_tup
  
  # Try connecting to YF and obtaining the data
  # On failure, print an error message
  try:
    yf_data = requests.get(yahoo_url).text.split("\n")[1:-1]
    prices = []
    for y in yf_data:
      p = y.strip().split(',')
  except Exception as e:
    print("Could not download Yahoo data: %s" % e)


if __name__ == "__main__":
  # This ignores warnings regarding Data Truncation from the Yahoo precision to Decimal (19,4) datatypes
  warnings.filterwarnings('ignore')
  
  # Loop over the tickers and insert the daily historical data into the db 
  tickers = obtain_list_of_db_tickers()
  lentickers = len(tickers)
  for i, t in enumerate(tickers):
    print("Adding data for %s: %s out of %s" % (t[1], i+1, lentickers))
    yf_data = get_daily_historic_data_yahoo(t[1])
