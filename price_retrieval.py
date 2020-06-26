import datetime
import warnings
import MySQLdb as mdb
import mysql.connector
import requests


# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
  cur = con.cursor()
  cur.execute("SELECT id, ticker FROM symbol")
  data = cur.fetchall()
  return [(d[0], d[1]) for d in data]

if __name__ == "__main__":
  tickers = obtain_list_of_db_tickers()
  print(len(tickers))
