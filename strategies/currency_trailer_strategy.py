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
from point_populator import PointPopulator
from db_manager import DBManager
from point import Point

class CurrencyTrailerStrategy:
	AMOUNT = 1
	TIME_PERIOD = 14400
	##delay looks at past avg in reference currency to predict target one in the present
	DELAY = 5 

	##possible modes
	SIMPLE = "SIMPLE"
	EXP = "EXP"

	##passed in predicter_currency_candles when strategy object is created
	##cur_traded_candles is updated later from trade_simulator
	def __init__(self, predicter_table_name, mode):
		self.cur_traded_candles = None
		self.predicter_table_name = predicter_table_name
		self.predicter_candles = Candle.get_candle_array(predicter_table_name)
		self.table_period = CandleTable.get_period(predicter_table_name)


		self.candles_to_skip = 0
		## if want to trade more often than data available, don't skip anything else skip however many table periods fit into TIME_PERIOD
		if self.table_period >= self.TIME_PERIOD:
			self.candles_to_skip = 1
		else:
			self.candles_to_skip = self.TIME_PERIOD/self.table_period

		##an array where avg at each time can be looked up
		self.point_avgs = self.create_table(predicter_table_name, mode)
	
	##returns market operation
	##time represents which candle the trade_simulator is processing atm
	def decide(self, time, bits):

		lookup_time = time - self.DELAY
		
		##only return a trade when time_period has passed and sufficient candles are skipped
		if lookup_time % self.candles_to_skip == 0 and lookup_time > self.candles_to_skip:
			##mv_past = MovingAverage(self.predicter_candles, (time-self.candles_to_skip))
			##mv_present = MovingAverage(self.predicter_candles, time)
			##avg_past = mv_past.simple()
			##avg_present = mv_present.simple()

			avg_past = self.point_avgs[lookup_time-self.candles_to_skip].value
			avg_present = self.point_avgs[lookup_time].value

			if avg_past < avg_present: ##trending up
				return Operation(Operation.BUY_OP, self.AMOUNT)
			elif avg_past > avg_present: ##trending down
				return Operation(Operation.SELL_OP, self.AMOUNT)
			elif avg_past == avg_present: ##stable trend
				return Operation(Operation.NONE_OP, 0)

		##do nothing rest of the time
		else:
			return Operation(Operation.NONE_OP, 0)

	##creates and populates a table where the avgs can then be looked up and then returns it
	def create_table(self, tn, mode):
		dbm = DBManager()
		if mode == self.SIMPLE:
			point_table_name = tn + PointPopulator.SIMPLE
		else:
			point_table_name = tn + PointPopulator.EXP

		if dbm.exists_table(point_table_name): ##if already exists, no need to populate
			pass
		else:
			##creates table
			pt = PointTable(point_table_name)
			pp.populate()
			
		return Point.get_point_array(point_table_name)	


