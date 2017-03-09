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
		print()
		print(("table_name: ", self.table_name))
		print(("date: ", self.date))
		print(("high: ", self.high))
		print(("low: ", self.low))
		print(("open: ", self.open))
		print(("close: ", self.close))
		print(("mid: ", self.mid))
		print(("volume: ", self.volume))
		print(("qvolume: ", self.quoteVolume))
		print(("wAvg: ", self.weightedAverage))
		print()

	
	##uses cursor tuple to create a Candle and return it
	@staticmethod
	def from_tuple(table_name, tup):
		c = Candle(table_name, tup[0], tup[1], tup[2], tup[3], tup[4], tup[6], tup[7], tup[8])
		return c

	def save(self):
		##look for duplicate, if it exists, update it instead of making another candle
		c = Candle.get_candle_by_date(self.table_name, self.date)
		if c is not None:
			c.update(self.high, self.low, self.open, self.close, self.mid, self.volume, self.quoteVolume, self.weightedAverage)
		else:
			dbm = DBManager.get_instance()
			cursor = dbm.get_cursor()
			try:
				cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_high}, {nf_low}, {nf_open}, {nf_close}, {nf_mid}, {nf_volume}, {nf_qVol}, {nf_wAvg}) VALUES\
						({v_date}, {v_high}, {v_low}, {v_open}, {v_close}, {v_mid}, {v_volume}, {v_qVol}, {v_wAvg})"\
					.format(tn = self.table_name, nf_date = self.DATE, nf_high = self.HIGH, nf_low = self.LOW, nf_open = self.OPEN, nf_close = self.CLOSE, nf_mid = self.MID, nf_volume = self.VOLUME, nf_qVol = self.QUOTE_VOLUME, nf_wAvg = self.WEIGHTED_AVERAGE, v_date = self.date, v_high = self.high, v_low = self.low, v_open = self.open, v_close = self.close, v_mid = self.mid, v_volume = self.volume, v_qVol = self.quoteVolume, v_wAvg = self.weightedAverage))
			except sqlite3.IntegrityError:
						print('ERROR: Something went wrong inserting candle into {tn}'.format(tn = table_name))

	def update(self, high, low, open, close, mid, volume, quoteVolume, weightedAverage):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "UPDATE {tn} SET {nf_high} = {v_high}, {nf_low} = {v_low}, {nf_open} = {v_open}, {nf_close} = {v_close}, {nf_mid} = {v_mid}, {nf_volume} = {v_volume}, {nf_qv} = {v_qv}, {nf_wa} = {v_wa}\
					WHERE {nf_date} = {v_date}"\
				.format(tn = self.table_name, nf_date = self.DATE, nf_high = self.HIGH, nf_low = self.LOW, nf_open = self.OPEN, nf_close = self.CLOSE, nf_mid = self.MID, nf_volume = self.VOLUME, nf_qv = self.QUOTE_VOLUME, nf_wa = self.WEIGHTED_AVERAGE, v_date = self.date, v_high = high, v_low = low, v_open = open, v_close = close, v_mid = mid, v_volume = volume, v_qv = quoteVolume, v_wa = weightedAverage)
			cursor.execute(exec_string)

		except sqlite3.IntegrityError:
			print('ERROR: Something went wrong updaing candle from {tn}'.format(tn = self.table_name))

	##return candle with matching date from given tablename
	@staticmethod
	def get_candle_by_date(tn, date):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute(("SELECT * FROM {tn} WHERE date = {v_date}").format(tn = tn, v_date = date))
		r = cursor.fetchone()
		if r is None:
			return None
		else:
			return Candle.from_tuple(tn, r)

