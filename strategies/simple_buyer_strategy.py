##simple buyer strategy
## buys every sixth candle, never sells

from operation import Operation

class SimpleBuyerStrategy:
	AMOUNT = 1

	def __init__(self):
		self.candles = None
	
	##returns market operation
	##time represents which candle the trade_simulator is processing atm
	def decide(self, time, bits):
		if time % 6 == 2:
			return Operation(Operation.BUY_OP, self.AMOUNT)
		else:
			##do nothing rest of the time
			return Operation(Operation.NONE_OP, 0)
