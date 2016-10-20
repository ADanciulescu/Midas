##helper calculates rate of change of graphs

from candle import Candle
from point import Point

class ROCCalculator:
	def __init__(self, dbm, pt_table_name, candles):
		self.candles = candles
		self.pt_table_name = pt_table_name
		self.dbm = dbm
	
	##returns array of pts corresponding to moving average of candles 
	def simple(self):
		
		##will eventually be returned
		pt_array = []

		for candle_index, c in enumerate(self.candles):
			## can't create ROC for i = 0
			roc = 0
			if candle_index == 0:
				roc = 0
			elif candle_index > 0:
				roc = self.candles[candle_index].mid - self.candles[candle_index-1].mid
			date = self.candles[candle_index].date
			pt = Point(self.dbm, self.pt_table_name, date, roc)
			pt_array.append(pt)
		return pt_array
