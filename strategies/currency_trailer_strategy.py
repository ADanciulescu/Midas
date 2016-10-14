##based on unverified theory based on assumptions:
## Assumption 1: Currency A correlates with currency B due to some hidden variable bias(different cryptos fall and rize together)
## Assumption 2: Currency A reacts faster to this hidden variable faster than Currency B
## Conclusion: Money can be made bytrading currency B while using the behaviour of currency A to predict its future behaviour

##Specific strategy:
##Set a constant time period
##Calculate moving average every time period, if currency A's avg is rising buy currency B, if not sell currency B

from operation import Operation
from moving_average import MovingAverage
from candle import Candle
from candle_table import CandleTable


class CurrencyTrailerStrategy:
	AMOUNT = 1
	TIME_PERIOD = 14400

	##passed in predicter_currency_candles when strategy object is created
	##cur_traded_candles is updated later from trade_simulator
	def __init__(self, predicter_table_name):
		self.cur_traded_candles = None
		self.predicter_table_name = predicter_table_name
		self.predicter_candles = Candle.get_candle_array(predicter_table_name)
		
		self.table_period = CandleTable.get_period(predicter_table)

		self.candles_to_skip = 0
		## if want to trade more often than data available, don't skip anything else skip however many table periods fit into TIME_PERIOD
		if self.table_period >= self.TIME_PERIOD:
			self.candles_to_skip = 1
		else:
			self.candles_to_skip = self.TIME_PERIOD/self.table_period
	
	##returns market operation
	##time represents which candle the trade_simulator is processing atm
	def decide(self, time, bits):
		##only return a trade when time_period has passed and sufficient candles are skipped
		if time % self.candles_to_skip == 0:
			mv_past = MovingAverage(predicter_candles, (time-self.candles_to_skip))
			mv_present = MovingAverage(predicter_candles, time)
			avg_past = mv_past.simple()
			avg_present = mv_present.simple()

			if avg_past < avg_present: ##trending up
				return Operation(Operation.BUY_OP, self.AMOUNT)
			elif avg_past > avg_presnet: ##trending down
				return Operation(Operation.SELL_OP, self.AMOUNT)
			elif avg_past == avg_presnet: ##stable trend
				return Operation(Operation.NONE_OP, 0)

		##do nothing rest of the time
		else:
			return Operation(Operation.NONE_OP, 0)


