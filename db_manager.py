import json
import sqlite3




class DBManager:
	def __init__(self):
		self.sqlfile = "./db/currencies.sqlite"
		self.conn = sqlite3.connect(self.sqlfile)
		

	##creates table for chart data
	##each row is a tick and holds data about the tick
	##columns: id, date, high, low, open, close, volume, quoteVolume, weightedAverage
	def create_data_table(self, data_name):
		cursor = self.conn.cursor()

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

		cursor.execute('CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY, {nf_date} {ft_i} {nn}, {nf_high} {ft_r} {nn}, {nf_low} {ft_r} {nn}, {nf_open} {ft_r} {nn}, {nf_close} {ft_r} {nn}, {nf_volume} {ft_r} {nn}, {nf_qVol} {ft_r} {nn}, {nf_wAvg} {ft_r} {nn})'\
				.format(tn = data_name, nf_id = col_id, nf_date = col_date, nf_high = col_high, nf_low = col_low, nf_open = col_open, nf_close = col_close, nf_volume = col_volume, nf_qVol = col_quoteVolume, nf_wAvg = col_weightedAverage, ft_i = ft_integer, ft_r = ft_real, nn = "NOT NULL"))
		self.conn.commit()
		self.conn.close()

	## drops the table by name
	def drop_table(self, table_name):
		cursor = self.conn.cursor()
		cursor.execute('DROP TABLE ' + table_name)
		self.conn.commit()
		self.conn.close()

