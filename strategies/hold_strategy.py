## buys at the beggining and then holds the currency, used to compare to actual strategy to normalize for natural trend in currency
from operation import Operation
from candle_table import CandleTable

class HoldStrategy:

	NAME = "HOLD"
	AMOUNT = 100

	def __init__(self, table_name):
		self.candles = CandleTable.get_candle_array(table_name)

	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits):
		
		if candle_num == 0:
			return Operation(Operation.BUY_OP, self.AMOUNT)
		else:
			return Operation(Operation.NONE_OP, 0)


