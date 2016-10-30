## uses google trends to predict when too buy and sell
## uses a short 2 day avg vs a 5 day avg in trends to get a buy/sell signal
## buys and sells when they cross

from point_populator import PointPopulator
from point_table import PointTable
from operation import Operation
from trade_logger import TradeLogger
from trade_table import TradeTable
from trade import Trade

class TwoAvgTrendStrategy():

	##constants for how many days to use to create the simple avg tables
	AVG_SHORT_DAYS = 3 
	AVG_LONG_DAYS = 20 

	DAY = 86400 ## secs in a day
	DELAY = 0 ## how many days in the past to look at trends to predict when to buy or sell

	BUY_AMOUNT = 100 ## amount of bits to buy when a buy signal is detected

	NAME = "AVG_TREND"

	def __init__(self, candle_table_name, trends_table_name):
		self.trends_table_name = trends_table_name
		self.cur_traded_candles = []
		self.candle_table_name = candle_table_name

		##create the 2 avg tables needed
		self.avg_table_name_short = self.create_avg_table(self.AVG_SHORT_DAYS)
		self.avg_table_name_long = self.create_avg_table(self.AVG_LONG_DAYS)

		self.trade_table = None

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
			cur_date = self.cur_traded_candles[time].date ##current date

			## if cur_date is too early to have valid trend data return no operation
			if not self.is_valid_date(cur_date):
				return Operation(Operation.NONE_OP, 0)

			
		
			trend_date_present = cur_date - self.DELAY * self.DAY ##date to lookup in trend table
			trend_date_past = trend_date_present - self.DAY ##date to lookup in trend table

			past_short_val = PointTable.lookup_date(self.avg_table_name_short, trend_date_past).value
			past_long_val = PointTable.lookup_date(self.avg_table_name_long, trend_date_past).value
			present_short_val = PointTable.lookup_date(self.avg_table_name_short, trend_date_present).value
			present_long_val = PointTable.lookup_date(self.avg_table_name_long, trend_date_present).value
			##detect intersection between the long and short trend tables
			if present_short_val >= present_long_val:
				if past_short_val >= past_long_val: ## no intersection
					return Operation(Operation.NONE_OP, 0)
				elif past_short_val < past_long_val: ## intersection with short term spike
					if self.is_valid_buy(cur_date):
						return Operation(Operation.BUY_OP, self.BUY_AMOUNT)
					else:
						return Operation(Operation.NONE_OP, 0)
			elif present_short_val <= present_long_val:
				if past_short_val <= past_long_val: ##no intersection
					return Operation(Operation.NONE_OP, 0)
				elif past_short_val > past_long_val: ## intersection with short term trough
					return Operation(Operation.SELL_OP, bits)


	##make sure date is late enough so that there is trend table data
	def is_valid_date(self, date):
		earliest_date = PointTable.lookup(self.avg_table_name_short, 1).date
		latest_date = PointTable.get_last(self.avg_table_name_short).date
		if (date - (self.DELAY+1)* self.DAY) < earliest_date:
			return False
		else:
			if date > latest_date:
				return False
			else:
				return True
	
	##makes sure that a buy signal is never used more than once
	def is_valid_buy(self, date):
		trades = TradeTable.get_trades_in_range(self.trade_table_name, date - self.DAY, date, Trade.BUY_TYPE)
		if len(trades) > 0:
			return False
		else:
			return True
