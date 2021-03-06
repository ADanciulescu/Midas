##simple test strategy
## buys 0.1 every sixth candle, sells every sixth candle 

from operation import Operation


class TestStrategy:
	AMOUNT = 1
	NAME = "TEST"

	def __init__(self):
		self.candles = None
	
	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	##time represents which candle the trade_simulator is processing atm
	def decide(self, time, bits):
		if time % 6 == 2:
			return Operation(Operation.BUY_OP, self.AMOUNT)
		elif time % 6 == 5:
			return Operation(Operation.SELL_OP, self.AMOUNT)
		else:
			##do nothing rest of the time
			return Operation(Operation.NONE_OP, 0)




