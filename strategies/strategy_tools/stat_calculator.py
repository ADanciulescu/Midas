##passed in candle table
##calculates useful stats about the candle table

from candle_table import CandleTable
from point_table import PointTable
from standard_deviation import StandardDeviation
from candle import Candle

class StatCalculator():
	
	def __init__(self, ct_name):
		self.ct_name = ct_name
		self.candles = CandleTable.get_candle_array(ct_name)
		
		self.pt_name_close = CandleTable.to_point_table(ct_name, Candle.CLOSE) 
		self.points_close = PointTable.get_point_array(self.pt_name_close)
		
		self.pt_name_volume = CandleTable.to_point_table(ct_name, Candle.VOLUME) 
		self.points_volume = PointTable.get_point_array(self.pt_name_volume)

	##returns volatility of candle table passed in
	## for now this is calculated simply as standard deviation
	def get_volatility(self):
		stddev = StandardDeviation.simple(self.points_close)
		return stddev/self.points_close[-1].value
	
	## returns volume of candle table passed in
	## for now it simply sums up all the volumes of each candle
	def get_volume(self):
		v_total = 0
		for p in self.points_volume:
			v_total+= p.value
		return v_total 
