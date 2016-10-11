## Model for a chart currency data tick
## can be created from json data or from db

##attributes: id, date, high, low, open, close, volume, quoteVolume, weightedAverage

from db_manager import DBManager
import json
import sqlite3

class ChartTick:
	##created ChartTick object from passed in data
	def __init__(self,db_manager, table_name, date, high, low, open, close, volume, quoteVolume, weightedAverage):
		self.table_name = table_name
		self.db_manager = db_manager

		self.date = date
		self.high = high
		self.low = low
		self.open = open
		self.close = close
		self.volume = volume
		self.quoteVolume = quoteVolume
		self.weightedAverage = weightedAverage
	
	
	##uses cursor tuple to create a ChartTick and return it
	@staticmethod
	def from_tuple(table_name, tup):
		dbm = DBManager()
		return ChartTick(dbm, table_name, tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])

	def save(self):
		cursor = self.db_manager.conn.cursor()
		try:
			cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_high}, {nf_low}, {nf_open}, {nf_close}, {nf_volume}, {nf_qVol}, {nf_wAvg}) VALUES\
					({v_date}, {v_high}, {v_low}, {v_open}, {v_close}, {v_volume}, {v_qVol}, {v_wAvg})"\
				.format(tn = self.table_name, nf_date = DBManager.col_date, nf_high = DBManager.col_high, nf_low = DBManager.col_low, nf_open = DBManager.col_open, nf_close = DBManager.col_close, nf_volume = DBManager.col_volume, nf_qVol = DBManager.col_quoteVolume, nf_wAvg = DBManager.col_weightedAverage, v_date = self.date, v_high = self.high, v_low = self.low, v_open = self.open, v_close = self.close, v_volume = self.volume, v_qVol = self.quoteVolume, v_wAvg = self.weightedAverage))
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting tick into {tn}'.format(tn = table_name))

