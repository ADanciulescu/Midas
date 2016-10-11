import json
import sqlite3




class DBManager:
	col_id = "id"
	col_date = "date"
	col_high = "high"
	col_low = "low"
	col_open = "open"
	col_close = "close"
	col_volume = "volume"
	col_quoteVolume = "quoteVolume"
	col_weightedAverage = "weightedAverage"

	ft_integer = "INTEGER"
	ft_real = "REAL"
	
	def __init__(self):
		self.sqlfile = "./db/currencies.sqlite"
		self.conn = sqlite3.connect(self.sqlfile)
		

	##creates table for chart data
	##each row is a tick and holds data about the tick
	##columns: id, date, high, low, open, close, volume, quoteVolume, weightedAverage
	def create_tick_table(self, table_name):
		self.conn = sqlite3.connect(self.sqlfile)
		cursor = self.conn.cursor()


		cursor.execute('CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY {nn}, {nf_date} {ft_i} {nn}, {nf_high} {ft_r} {nn}, {nf_low} {ft_r} {nn}, {nf_open} {ft_r} {nn}, {nf_close} {ft_r} {nn}, {nf_volume} {ft_r} {nn}, {nf_qVol} {ft_r} {nn}, {nf_wAvg} {ft_r} {nn})'\
				.format(tn = table_name, nf_id = self.col_id, nf_date = self.col_date, nf_high = self.col_high, nf_low = self.col_low, nf_open = self.col_open, nf_close = self.col_close, nf_volume = self.col_volume, nf_qVol = self.col_quoteVolume, nf_wAvg = self.col_weightedAverage, ft_i = self.ft_integer, ft_r = self.ft_real, nn = "NOT NULL"))
		self.conn.commit()
		self.conn.close()

	##returns cursor to all ticks in table_name)
	def get_tick_cursor(self, table_name):
		self.conn = sqlite3.connect(self.sqlfile)
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor



	## drops the table by name
	def drop_table(self, table_name):
		self.conn = sqlite3.connect(self.sqlfile)
		cursor = self.conn.cursor()
		cursor.execute('DROP TABLE ' + table_name)
		self.conn.commit()
		self.conn.close()

	##returns true if table exists otherwise false
	def exists_table(self, table_name):
		self.conn = sqlite3.connect(self.sqlfile)
		cursor = self.conn.cursor()
		exec_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}'".format(tn = table_name)
		cursor.execute(exec_string)
		if cursor > 0:
			return True
		else:
			return False

