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

	AMOUNT = 10
	NAME = "BOLLINGER"


	##constant string used to specifiy type of bollinger band
	LOW = "LOW"
	HIGH = "HIGH"

	def __init__(self, candles, bb_factor = 2, stddev_adjust = True, avg_period = 40, num_past_buy = 0, num_past_sell = 0):
		
		##model parameters
		self.bb_factor = bb_factor ##number of standard deviations of difference between a bollinger band and the avg
		self.stddev_adjust = stddev_adjust ## if true adjust amount bought/sold by how much it deviates from the bollinger band, if false use constant amount
		self.avg_period = avg_period ## how many candles to use to make avg
		self.num_past_buy = num_past_buy ## how long to plan buying before actually buying
		self.num_past_sell = num_past_sell ## how long to plan selling before actually selling



		##NOTE: removed extra parameter for stddev_period, currently same as avg_period
		##self.stddev_period = stddev_period ##how many past candles to use to compute stddeviation

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
		self.middle_avg_table_name = pp.create_moving_avg_simple(self.avg_period)
		self.avg_pts = PointTable.get_point_array(self.middle_avg_table_name)
		
		##create standard deviation line
		pp = PointPopulator(self.candle_table_name)
		pp.setup()
		self.stddev_table_name = pp.create_stddev(self.avg_period)
		self.stddev_pts = PointTable.get_point_array(self.stddev_table_name)

		##create bollinger band tables
		self.bb_low_name = self.create_bb(self.LOW)
		self.bb_high_name = self.create_bb(self.HIGH)

		self.bb_low_pts = PointTable.get_point_array(self.bb_low_name)
		self.bb_high_pts = PointTable.get_point_array(self.bb_high_name)

	## return difference in terms of standard deviations between last candle value and bollinger bands
	## 0 means on avg, positive value is how many standard deviations above average, negative value is for below average
	def get_present_bollinger_diff(self):
		cur_value = self.candles[-1].close
		last_candle_index = len(self.candles) - 1
		avg = self.avg_pts[last_candle_index - 1].value
		stddev = self.stddev_pts[last_candle_index - self.avg_period - 1].value
		return (cur_value-avg)/stddev



	##delete tables that were created
	def cleanup(self):
		self.dbm.drop_table(self.middle_avg_table_name)
		self.dbm.drop_table(self.stddev_table_name)
		self.dbm.drop_table(self.bb_low_name)
		self.dbm.drop_table(self.bb_high_name)

	##creates bollinger band table
	##type is either low or high
	def create_bb(self, type):
		bb_table_name = self.middle_avg_table_name + "_" + type
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(bb_table_name):
			DBManager.drop_table(bb_table_name)
		
		bb_pt_table = PointTable(bb_table_name)
		bb_pt_table.save()


		for i, avg in enumerate(self.avg_pts):
			if i < self.avg_period:
				pass
			else:
				date = avg.date
				if type == self.LOW:
					value = avg.value - (self.bb_factor * self.stddev_pts[i-self.avg_period].value) 
				elif type == self.HIGH:
					value = avg.value + (self.bb_factor * self.stddev_pts[i-self.avg_period].value)

				new_pt = Point(self.dbm, bb_table_name, date, value)
				new_pt.save()
		self.dbm.save_and_close()
		self.dbm = DBManager()
		return bb_table_name

	##returns market operation
	def decide(self, candle_num, bits):
		date = self.candles[candle_num].date
		amount = self.AMOUNT
		price = self.candles[candle_num].close

		##don't trade for first period that does not have adequate history
		if candle_num <= self.avg_period:
			self.trade_plan_array.append(TradePlan(date, 0, price, TradePlan.NONE))
			return Operation(Operation.NONE_OP, 0)
		else:
			##if current price exceeds high bollinger band -> sell
			if self.candles[candle_num].close > self.bb_high_pts[candle_num - self.avg_period -1].value:
				##thinking of selling, before actually selling make sure selling was planned for at least num_past_sell
				if TradePlan.check_past(self.trade_plan_array, candle_num, self.num_past_sell, TradePlan.PLAN_SELL):
					
					if self.stddev_adjust:
						##scale amount sold by factor determined by how much price is deviating from the bollinger band
						price_difference = self.candles[candle_num].close - self.bb_high_pts[candle_num - self.avg_period -1].value
						factor = price_difference/ self.stddev_pts[candle_num - self.avg_period- 1].value
						amount = self.AMOUNT * factor 

					self.trade_plan_array.append(TradePlan(date, amount, price, TradePlan.PLAN_SELL))
					return Operation(Operation.SELL_OP, amount)
				else:
					self.trade_plan_array.append(TradePlan(date, amount, price, TradePlan.PLAN_SELL))
					return Operation(Operation.NONE_OP, 0)

			##if current price is below low bollinger band -> buy
			elif self.candles[candle_num].close < self.bb_low_pts[candle_num - self.avg_period -1].value:
				##thinking of buying, before actually buying make sure buying was planned for at least num_past_buy
				if TradePlan.check_past(self.trade_plan_array, candle_num, self.num_past_buy, TradePlan.PLAN_BUY):
					
					if self.stddev_adjust:
						##scale amount bought by factor determined by how much price is deviating from the bollinger band
						price_difference = self.bb_low_pts[candle_num - self.avg_period -1].value - self.candles[candle_num].close
						factor = price_difference/ self.stddev_pts[candle_num - self.avg_period- 1].value
						amount = self.AMOUNT * factor
					

					self.trade_plan_array.append(TradePlan(date, amount, price, TradePlan.PLAN_BUY))
					return Operation(Operation.BUY_OP, amount)
				else:
					self.trade_plan_array.append(TradePlan(date, amount, price, TradePlan.PLAN_BUY))
					return Operation(Operation.NONE_OP, 0)

			else:
				self.trade_plan_array.append(TradePlan(date, 0, price, TradePlan.NONE))
				return Operation(Operation.NONE_OP, 0)
