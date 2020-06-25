from __future__ import print_function
import datetime
from math import ceil
import bs4
import MySQLdb as mdb
import requests

def obtain_parse_wiki_snp500():
  """
  Download and parse the Wikipedia list of S&P 500 constituents
  Using requests and BeautifulSoup

  Returns a list of tuples to add to MySQL db
  """
  # Stores the current time, for the created_at record
  now = datetime.datetime.utcnow()

  # Use requests and bs4 to download the list of S&P500 Companies and obtain symbol table
  response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
  soup = bs4.BeautifulSoup(response.text)
  
  # Select the first table (using CSS selector syntax) and ignore the header row 
  symbols_list = soup.select('table')[0].select('tr')[1:]

  # Obtain the symbol info for each row in the S&P500 constituent table
  symbols = []
  for i, symbol in enumerate(symbols_list):
    tds = symbol.select('td')
    ticker = tds[0].select('a')[0].text
    name = tds[1].select('a')[0].text
    sector = tds[3].text
    symbols.append(ticker, 'stock', name, sector, 'USD', now, now)
  
  return symbols


def insert_snp500_symbols(symbols):
  """
  
  """
    

if __name__ == "__main__":
  symbols = obtain_parse_wiki_snp500()
  
