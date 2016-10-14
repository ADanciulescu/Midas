import json
import sqlite3

class DBManager:

	INTEGER = "INTEGER"
	REAL = "REAL"
	NOT_NULL = "NOT NULL"
	
	def __init__(self):
		self.sqlfile = "./db/currencies.sqlite"
		self.conn = sqlite3.connect(self.sqlfile)
		
	##commit changes to db and close DBManager instance
	def save_and_close(self):
		self.conn.commit()
		self.conn.close()

	def get_cursor(self):
		return self.conn.cursor()


	##returns cursor to all candles in table_name)
	def get_candle_cursor(self, table_name):
		self.conn = sqlite3.connect(self.sqlfile)
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor


