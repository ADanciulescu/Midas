##Uses a scipy model created and trained somewhere else to decide trades 

from sklearn.neural_network import MLPClassifier
from operation import Operation
from moving_average import MovingAverage
from candle import Candle
from candle_table import CandleTable
from point_populator import PointPopulator
from trend_cutter import TrendCutter
from trend_table import TrendTable
from db_manager import DBManager
from point import Point

class ScipyTrendModelStrategy:

	AMOUNT = 10
	TIME_PERIOD = 14400
	NAME = "SCIPY_MODEL"

	def __init__(self, candle_table_name, trend_table_name, neural_model):
		self.cur_traded_candles = None
		self.neural_model = neural_model
		tc = TrendCutter(candle_table_name, trend_table_name)
		trend_table = tc.create_cut_table()
		self.trends = TrendTable.get_trend_array(trend_table.table_name)
	
	
	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	##candle_num represents which candle the trade_simulator is processing atm
	def decide(self, candle_num, bits):
		if candle_num > self.neural_model.num_past:
			
			##computing what will be the input into the model
			inp = []
			for i in range(self.neural_model.num_past):
				inp.append(self.trends[candle_num- (self.neural_model.num_past - i)].hits)
			
			##get model prediction
			results = self.neural_model.model.predict([inp])
			result = results[0]
			
			if result == 1: ##trending up
				return Operation(Operation.BUY_OP, self.AMOUNT)
			elif result == -1: ##trending down
				return Operation(Operation.SELL_OP, self.AMOUNT)
			elif result == 0: ##stable trend
				return Operation(Operation.NONE_OP, 0)
		else:
			return Operation(Operation.NONE_OP, 0)


