## trades randomly, used to compare to actual strategy to normalize for natural trend in currency
from random import randint
from operation import Operation

class RandomStrategy:

	NAME = "RANDOM"
	AMOUNT = 10

	def __init__(self, candles):
		self.candles = candles

	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits):
		
		## -1 means sell, 0 means do nothing, 1 means buy
		rand_num = randint(-1, 1)

		if rand_num == -1:
			return Operation(Operation.SELL_OP, self.AMOUNT)
		elif rand_num == 0:
			return Operation(Operation.BUY_OP, self.AMOUNT)
		elif rand_num == 1:
			return Operation(Operation.NONE_OP, 0)
