## presents trend history and asks for user input to manuall trade

from operation import Operation
from trade_logger import TradeLogger
from trade_table import TradeTable
from trade import Trade
from tools import timestamp_to_date
from trend_table import TrendTable

class ManualAttributeStrategy():

	DAY = 86400 ## secs in a day
	BUY_AMOUNT = 100 ## amount of bits to buy when a buy signal is detected
	NAME = "MANUAL_ATTRIBUTE"

	BUY_CMD = "b"
	SELL_CMD = "s"
	NONE_CMD = "n"


	def __init__(self, candles, attribute_name):
		self.candles = candles
		self.attribute_name = attribute_name
		
	##simply returns name
	def get_name(self):
		return  self.NAME
	

	##returns market operation
	##time represents which candle the trade_simulator is processing atm
	def decide(self, time, bits):
		print("************************************************************************************************")
		print(("Time: ", timestamp_to_date(self.candles[time].date)))
		print(("Price: ", self.candles[time].close))
		print((self.attribute_name, ": ", getattr(self.candles[time], self.attribute_name)))

		## ask for user input
		response = raw_input("Please enter trade: ")
		print("************************************************************************************************")
		if response == self.BUY_CMD:
			return Operation(Operation.BUY_OP, self.BUY_AMOUNT)
		elif response == self.SELL_CMD:
			return Operation(Operation.SELL_OP, bits)
		else:
			return Operation(Operation.NONE_OP, 0)



