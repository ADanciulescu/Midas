## Model for a chart currency data candle 
## can be created from json data or from db

##attributes: id, date, high, low, open, close, mid, volume, quoteVolume, weightedAverage

import json
import sqlite3
from db_manager import DBManager
from candle_table import CandleTable

class Candle:
	##created Candle object from passed in data
	def __init__(self,db_manager, table_name, date, high, low, open, close, volume, quoteVolume, weightedAverage):
		self.table_name = table_name
		self.db_manager = db_manager

		self.date = date
		self.high = high
		self.low = low
		self.open = open
		self.close = close
		self.mid = (close+open)/2
		self.volume = volume
		self.quoteVolume = quoteVolume
		self.weightedAverage = weightedAverage
	
	
	##uses cursor tuple to create a Candle and return it
	@staticmethod
	def from_tuple(table_name, tup):
		dbm = DBManager()
		return Candle(dbm, table_name, tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])

	def save(self):
		cursor = self.db_manager.get_cursor()
		try:
			cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_high}, {nf_low}, {nf_open}, {nf_close}, {nf_mid}, {nf_volume}, {nf_qVol}, {nf_wAvg}) VALUES\
					({v_date}, {v_high}, {v_low}, {v_open}, {v_close}, {v_mid}, {v_volume}, {v_qVol}, {v_wAvg})"\
				.format(tn = self.table_name, nf_date = CandleTable.DATE, nf_high = CandleTable.HIGH, nf_low = CandleTable.LOW, nf_open = CandleTable.OPEN, nf_close = CandleTable.CLOSE, nf_mid = CandleTable.MID, nf_volume = CandleTable.VOLUME, nf_qVol = CandleTable.QUOTE_VOLUME, nf_wAvg = CandleTable.WEIGHTED_AVERAGE, v_date = self.date, v_high = self.high, v_low = self.low, v_open = self.open, v_close = self.close, v_mid = self.mid, v_volume = self.volume, v_qVol = self.quoteVolume, v_wAvg = self.weightedAverage))
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting candle into {tn}'.format(tn = table_name))


	##returns candle objects for the given table_name
	@staticmethod
	def get_candle_array(table_name):
		db_manager = DBManager()

		##returns a cursor pointing to all candles linked to the table_name
		cursor = db_manager.get_candle_cursor(table_name)
		
		candles = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Candle.from_tuple(table_name, row) 
			candles.append(t)
			row = cursor.fetchone()
		return candles
