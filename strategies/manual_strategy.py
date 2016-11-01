## presents trend history and asks for user input to manuall trade

from point_populator import PointPopulator
from point_table import PointTable
from operation import Operation
from trade_logger import TradeLogger
from trade_table import TradeTable
from trade import Trade
from tools import timestamp_to_date
from trend_table import TrendTable

class ManualStrategy():

	DAY = 86400 ## secs in a day
	BUY_AMOUNT = 100 ## amount of bits to buy when a buy signal is detected
	NAME = "MANUAL_TREND"

	BUY_CMD = "b"
	SELL_CMD = "s"
	NONE_CMD = "n"

	DELAY = 1 ## how many days in the past to look at trends to predict when to buy or sell

	AVG_PERIOD = 1 ## period(in days) to create moving average of trend table

	def __init__(self, candle_table_name, trends_table_name):
		self.trends_table_name = trends_table_name
		self.cur_traded_candles = []
		self.candle_table_name = candle_table_name
		self.trade_table = None
		self.trend_table = TrendTable.get_trend_array(trends_table_name)
		self.avg_table_name = self.create_avg_table(self.AVG_PERIOD)

		## make sure only prompted for trade every new day
		self.last_date = None
		
	##simply returns name
	def get_name(self):
		return  self.NAME
	
	##creates avg point table for the given period
	def create_avg_table(self, period):	
		pp = PointPopulator(self.trends_table_name)
		return pp.create_moving_avg_simple(period)

	##returns market operation
	##time represents which candle the trade_simulator is processing atm
	def decide(self, time, bits):
			cur_timestamp = self.cur_traded_candles[time].date 
			trend_timestamp = cur_timestamp - self.DELAY*self.DAY
			cur_date = timestamp_to_date(cur_timestamp)

			if cur_date != self.last_date:
				self.last_date = cur_date

				try:
					past_avg = PointTable.lookup_date(self.avg_table_name, trend_timestamp).value
					print "Number of views: " + str(past_avg) 
				except:
					return Operation(Operation.NONE_OP, 0)

				## ask for user input
				response = raw_input("Please enter trade: ")
				if response == self.BUY_CMD:
					return Operation(Operation.BUY_OP, self.BUY_AMOUNT)
				elif response == self.SELL_CMD:
					return Operation(Operation.SELL_OP, bits)
				else:
					return Operation(Operation.NONE_OP, 0)
			else:
				return Operation(Operation.NONE_OP, 0)



