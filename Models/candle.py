## Model for a chart currency data candle 
## can be created from tuple data or from db

##attributes: date, high, low, open, close, mid, volume, quoteVolume, weightedAverage

import sqlite3
from db_manager import DBManager

class Candle:
	DATE = "date"
	HIGH = "high"
	LOW = "low"
	OPEN = "open"
	CLOSE = "close"
	MID = "mid"
	VOLUME = "volume"
	QUOTE_VOLUME = "quoteVolume"
	WEIGHTED_AVERAGE = "weightedAverage"
	
	##created Candle object from passed in data
	def __init__(self, table_name, date, high, low, open, close, volume, quoteVolume, weightedAverage):
		self.table_name = table_name
		self.date = date
		self.high = high
		self.low = low
		self.open = open
		self.close = close
		self.mid = (close+open)/2
		self.volume = volume
		self.quoteVolume = quoteVolume
		self.weightedAverage = weightedAverage

	def pprint(self):
		print ""
		print "table_name: ", self.table_name
		print "date: ", self.date
		print "high: ", self.high
		print "low: ", self.low
		print "open: ", self.open
		print "close: ", self.close
		print "mid: ", self.mid
		print "volume: ", self.volume
		print "qvolume: ", self.quoteVolume
		print "wAvg: ", self.weightedAverage
		print ""

	
	##uses cursor tuple to create a Candle and return it
	@staticmethod
	def from_tuple(table_name, tup):
		c = Candle(table_name, tup[0], tup[1], tup[2], tup[3], tup[4], tup[6], tup[7], tup[8])
		return c

	def save(self):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		try:
			cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_high}, {nf_low}, {nf_open}, {nf_close}, {nf_mid}, {nf_volume}, {nf_qVol}, {nf_wAvg}) VALUES\
					({v_date}, {v_high}, {v_low}, {v_open}, {v_close}, {v_mid}, {v_volume}, {v_qVol}, {v_wAvg})"\
				.format(tn = self.table_name, nf_date = self.DATE, nf_high = self.HIGH, nf_low = self.LOW, nf_open = self.OPEN, nf_close = self.CLOSE, nf_mid = self.MID, nf_volume = self.VOLUME, nf_qVol = self.QUOTE_VOLUME, nf_wAvg = self.WEIGHTED_AVERAGE, v_date = self.date, v_high = self.high, v_low = self.low, v_open = self.open, v_close = self.close, v_mid = self.mid, v_volume = self.volume, v_qVol = self.quoteVolume, v_wAvg = self.weightedAverage))
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting candle into {tn}'.format(tn = table_name))


