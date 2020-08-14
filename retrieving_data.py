import pandas as pd
import MySQLdb as mdb

if __name__ == "__main__":
  # Connect to the MySQL instance
  db_host = 'localhost'
  db_user = 'sec_user'
  db_pass = 'password'
  db_name = 'securities_master'
  con = mdb.connect(db_host, db_user, db_pass, db_name)

  # Select all of the Google adjusted close data
  sql = """SELECT dp.price_date, dp.adj_close_price 
	FROM symbol as sym 
	INNER JOIN daily_price AS dp 
	ON dp.symbol_id = sym.id 
	WHERE sym.ticker = 'GOOG'
	ORDER BY dp.price_date ASC;"""

  # Create a pandas DF from the SQL query
  goog = pd.read_sql_query(sql, con=con, index_col='price_date')

  # Output the DF head
  print(goog.head())
