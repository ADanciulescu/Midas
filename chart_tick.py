## Model for a chart currency data tick
## can be created from json data or from db

##attributes: id, date, high, low, open, close, volume, quoteVolume, weightedAverage

from db_manager import DBManager
import json
import sqlite3

class ChartTick:
	##created ChartTick object from json data entry
	def __init__(self, table_name, json):
		self.table_name = table_name

		self.date = json["date"]
		self.high = json["high"]
		self.low = json["low"]
		self.open = json["open"]
		self.close = json["close"]
		self.volume = json["volume"]
		self.quoteVolume = json["quoteVolume"]
		self.weightedAverage = json["weightedAverage"]

	def save(self):
		db_manager = DBManager()
		cursor = db_manager.conn.cursor()
		try:
			cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_high}, {nf_low}, {nf_open}, {nf_close}, {nf_volume}, {nf_qVol}, {nf_wAvg}) VALUES\
					({v_date}, {v_high}, {v_low}, {v_open}, {v_close}, {v_volume}, {v_qVol}, {v_wAvg})"\
				.format(tn = self.table_name, nf_date = DBManager.col_date, nf_high = DBManager.col_high, nf_low = DBManager.col_low, nf_open = DBManager.col_open, nf_close = DBManager.col_close, nf_volume = DBManager.col_volume, nf_qVol = DBManager.col_quoteVolume, nf_wAvg = DBManager.col_weightedAverage, v_date = self.date, v_high = self.high, v_low = self.low, v_open = self.open, v_close = self.close, v_volume = self.volume, v_qVol = self.quoteVolume, v_wAvg = self.weightedAverage))
			
			db_manager.conn.commit()
			db_manager.conn.close()
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting tick into {tn}'.format(tn = table_name))

