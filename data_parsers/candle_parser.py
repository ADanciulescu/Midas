## adds candles to table

from candle import Candle
from db_manager import DBManager

class CandleParser:
	def __init__(self, table_name, data):
		self.table_name = table_name
		self.data = data

		self.insert()
	
	def insert(self):
		for c in self.data:
			try:
				ct = Candle(self.table_name, c['date'], c['high'], c['low'], c['open'], c['close'], c['volume'], c['quoteVolume'], c['weightedAverage'])
				try:
					ct.save()
				except:
						"Duplicate candle, cannot insert"
			except:
				print("Candle cannot be parsed")
		dbm = DBManager.get_instance()
		dbm.save_and_close()


