## computes bollinger bands to decide when to sell and when to buy
## crossing the lower band signals buy and crossing upper band signals sell

from operation import Operation
from moving_average import MovingAverage
from candle import Candle
from candle_table import CandleTable
from point_populator import PointPopulator
from db_manager import DBManager
from point import Point
from point_populator import PointPopulator
from point_table import PointTable
from db_manager import DBManager
from trade import Trade
from trade_table import TradeTable
from trade_plan import TradePlan

class BollingerStrategy:

	BUY_LIMIT = 86400 ##how long to wait until another buy signal can be accepted 
	AMOUNT = 10
	NAME = "BOLLINGER"
	AVG_PERIODS = 30 ## how many candles to use to make avg
	STDDEV_PERIODS = 30 ##how many past candles to use to compute stddeviation
	##number of standard deviations of difference between bollinger bands and avg
	BB_FACTOR = 2.5

	NUM_PAST_BUY = 2 ## how long to plan buying before actually buying
	NUM_PAST_SELL = 86400 ## how long to plan selling before actually selling

	##constant string used to specifiy type of bollinger band
	LOW = "LOW"
	HIGH = "HIGH"

	def __init__(self, candles):
		self.candles = candles
		self.trade_table = None
		self.trade_plan_array = []
		self.dbm = DBManager()
		self.candle_table_name = candles[0].table_name	
		self.create_tables()
		self.cleanup()

	##simply returns name
	def get_name(self):
		return  self.NAME

	##create tables for bollinger bands as well as table for mid avg
	def create_tables(self):
		
		## create mid avg table
		pp = PointPopulator(self.candle_table_name)
		pp.setup()
		self.middle_avg_table_name = pp.create_moving_avg_simple(self.AVG_PERIODS)
		
		##create standard deviation line
		pp = PointPopulator(self.candle_table_name)
		pp.setup()
		self.stddev_table_name = pp.create_stddev(self.AVG_PERIODS)

		##create bollinger band tables
		self.bb_low_name = self.create_bb(self.LOW, self.middle_avg_table_name, self.stddev_table_name)
		self.bb_high_name = self.create_bb(self.HIGH, self.middle_avg_table_name, self.stddev_table_name)

		self.bb_low_pts = PointTable.get_point_array(self.bb_low_name)
		self.bb_high_pts = PointTable.get_point_array(self.bb_high_name)

	##delete tables that were created
	def cleanup(self):
		self.dbm.drop_table(self.middle_avg_table_name)
		self.dbm.drop_table(self.stddev_table_name)
		self.dbm.drop_table(self.bb_low_name)
		self.dbm.drop_table(self.bb_high_name)

	##creates bollinger band table
	##type is either low or high
	def create_bb(self, type, avg_table_name, stddev_table_name):
		bb_table_name = avg_table_name + "_" + type
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(bb_table_name):
			DBManager.drop_table(bb_table_name)
		
		bb_pt_table = PointTable(bb_table_name)
		bb_pt_table.save()

		avg_pts = PointTable.get_point_array(avg_table_name)
		stddev_pts = PointTable.get_point_array(stddev_table_name)

		for i, avg in enumerate(avg_pts):
			if i < self.AVG_PERIODS:
				pass
			else:
				date = avg.date
				if type == self.LOW:
					value = avg.value - (self.BB_FACTOR * stddev_pts[i-self.AVG_PERIODS].value) 
				elif type == self.HIGH:
					value = avg.value + (self.BB_FACTOR * stddev_pts[i-self.AVG_PERIODS].value)

				new_pt = Point(self.dbm, bb_table_name, date, value)
				new_pt.save()
		self.dbm.save_and_close()
		self.dbm = DBManager()
		return bb_table_name

	##returns market operation
	def decide2(self, candle_num, bits):

		date = self.candles[candle_num].date
		amount = self.AMOUNT
		price = self.candles[candle_num].close

		##don't trade for first period that does not have adequate history
		if candle_num <= self.AVG_PERIODS:
			type = TradePlan.NONE
			tp = TradePlan(date, amount, price, type)
			self.trade_plan_array.append(tp)
			return Operation(Operation.NONE_OP, 0)
		else:
			##if current price exceeds high bollinger band -> buy
			if self.candles[candle_num].close > self.bb_high_pts[candle_num - self.AVG_PERIODS -1].value:
				type = TradePlan.SELL
				tp = TradePlan(date, amount, price, type)
				self.trade_plan_array.append(tp)
				return Operation(Operation.SELL_OP, self.AMOUNT)
			##if current price is below low bollinger band -> sell
			elif self.candles[candle_num].close < self.bb_low_pts[candle_num - self.AVG_PERIODS -1].value:
				if TradePlan.check_past(self.trade_plan_array, candle_num, self.NUM_PAST_BUY, TradePlan.PLAN_BUY):
					type = TradePlan.BUY
					tp = TradePlan(date, amount, price, type)
					self.trade_plan_array.append(tp)
					return Operation(Operation.BUY_OP, self.AMOUNT)
				else:
					type = TradePlan.PLAN_BUY
					tp = TradePlan(date, amount, price, type)
					self.trade_plan_array.append(tp)
					return Operation(Operation.NONE_OP, 0)

			else:
				type = TradePlan.NONE
				tp = TradePlan(date, amount, price, type)
				self.trade_plan_array.append(tp)
				return Operation(Operation.NONE_OP, 0)

	##returns market operation
	def decide(self, candle_num, bits):
		##don't trade for first period that does not have adequate history
		if candle_num <= self.AVG_PERIODS:
			return Operation(Operation.NONE_OP, 0)
		else:
			##if current price exceeds high bollinger band -> buy
			if self.candles[candle_num].close > self.bb_high_pts[candle_num - self.AVG_PERIODS -1].value:
				return Operation(Operation.SELL_OP, self.AMOUNT)
			##if current price is below low bollinger band -> sell
			elif self.candles[candle_num].close < self.bb_low_pts[candle_num - self.AVG_PERIODS -1].value:
				date = self.candles[candle_num].date
				##if self.is_valid_buy(date):
				return Operation(Operation.BUY_OP, self.AMOUNT)
				##else:
					##return Operation(Operation.NONE_OP, 0)
			else:
				return Operation(Operation.NONE_OP, 0)

	##makes sure that a buy signal is not duplicated before a sufficient time has passed 
	##def is_valid_buy(self, date):
		##trades = TradeTable.get_trades_in_range(self.trade_table_name, date - self.BUY_LIMIT, date, Trade.BUY_TYPE)
		##if len(trades) > 0:
			##return False
		##else:
			return True
