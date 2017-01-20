##Uses a scipy model created and trained somewhere else to decide trades 

from operation import Operation
from moving_average import MovingAverage
from candle import Candle
from candle_table import CandleTable
from point_populator import PointPopulator
from db_manager import DBManager
from point import Point

class ScipyCandleModelStrategy:

	AMOUNT = 10
	TIME_PERIOD = 14400
	NAME = "SCIPY_CANDLEMODEL"

	def __init__(self, candle_table_name, neural_model):
		self.cur_traded_candles = None
		self.neural_model = neural_model
		self.candles = CandleTable.get_candle_array(candle_table_name)
	
	
	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	##candle_num represents which candle the trade_simulator is processing atm
	def decide(self, candle_num, bits):

		##make sure there exists adequate history for prediction, return NONE OP
		if candle_num > self.neural_model.num_past:
			
			##computing what will be the input into the model
			inp = []
			for i in range(self.neural_model.num_past):
				if self.neural_model.mode == self.neural_model.CLOSE:
					inp.append(self.candles[candle_num- (self.neural_model.num_past - i)].close)
				elif self.neural_model.mode == self.neural_model.VOLUME:
					inp.append(self.candles[candle_num- (self.neural_model.num_past - i)].volume)
			
			##get model prediction
			results = self.neural_model.model.predict([inp])
			result = results[0]
			
			if result == 1: 
				return Operation(Operation.BUY_OP, self.AMOUNT)
			elif result == -1: 
				return Operation(Operation.SELL_OP, self.AMOUNT)
			elif result == 0: 
				return Operation(Operation.NONE_OP, 0)
		else:
			return Operation(Operation.NONE_OP, 0)


