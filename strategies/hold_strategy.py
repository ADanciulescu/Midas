## buys at the beggining and then holds the currency, used to compare to actual strategy to normalize for natural trend in currency
from operation import Operation
from candle_table import CandleTable
from trade_simulator import TradeSimulator

class HoldStrategy:

	NAME = "HOLD"

	def __init__(self, table_name, to_spend):
		self.candles = CandleTable.get_candle_array(table_name)
		num_candles = len(self.candles)
		period = float(CandleTable.get_period(table_name))
		self.amount = to_spend/(self.candles[0].close*(1+TradeSimulator.BUY_FEE))

	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits, balance):
		
		if candle_num == 0:
			return Operation(Operation.BUY_OP, self.amount)
		else:
			return Operation(Operation.NONE_OP, 0)


