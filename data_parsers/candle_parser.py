## adds candles to table

from candle import Candle
from db_manager import DBManager

class CandleParser:
	def __init__(self, table_name, data):
		self.table_name = table_name
		self.data = data

		self.insert()
	
	def insert(self):
		db_manager = DBManager()
		for c in self.data:
			ct = Candle(db_manager, self.table_name, c['date'], c['high'], c['low'], c['open'], c['close'], c['volume'], c['quoteVolume'], c['weightedAverage'])
			try:
				ct.save()
			except:
					"Duplicate candle, cannot insert"
		db_manager.conn.commit()
		db_manager.conn.close()



