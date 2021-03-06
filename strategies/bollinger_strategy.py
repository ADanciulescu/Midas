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
from trade_simulator import TradeSimulator
import math

class BollingerStrategy:

	NAME = "BOLLINGER"


	##constant string used to specifiy type of bollinger band
	LOW = "LOW"
	HIGH = "HIGH"
	ONE_OP_DELAY = 20 
	STANDARD_AMOUNT = 1

	def __init__(self, table_name, std_amount = False, bb_factor = 2.5, to_carry = True, one_op = True, stddev_adjust = True, wait_better = True,
			avg_period = 80, num_past_buy = 0, num_past_sell = 6, set_default = False, calc_stats = False):
		
		##model parameters
		self.bb_factor = bb_factor ##number of standard deviations of difference between a bollinger band and the avg
		self.to_carry = to_carry ##if set, when performing a buy/sell increase amount by the sum of all previous plan_buy/plan_sell
		self.one_op = one_op ##if set force a delay between operations of the same type
		self.stddev_adjust = stddev_adjust ## if true adjust amount bought/sold by how much it deviates from the bollinger band, if false use constant amount
		self.wait_better = wait_better ## if set to true only approve buys or sells if bb_score has improved since last buy or sell
		self.avg_period = avg_period ## how many candles to use to make avg
		self.num_past_buy = num_past_buy ## how long to plan buying before actually buying
		self.num_past_sell = num_past_sell ## how long to plan selling before actually selling
		self.set_default = set_default


		##NOTE: removed extra parameter for stddev_period, currently same as avg_period
		##self.stddev_period = stddev_period ##how many past candles to use to compute stddeviation
		self.table_name = table_name
		
		if std_amount:
			##used by actual trader that does it's own amount standardization
			self.amount = self.STANDARD_AMOUNT
		else:
			##used by simulator, adjusts amount based on currency
			self.amount = TradeSimulator.get_currency_amount(table_name)
		self.candles = CandleTable.get_candle_array(table_name)
		self.trade_table = None
		self.trade_plan_array = []
		self.bb_scores = []
		self.candle_table_name = table_name
		if self.set_default:
			self.set_defaults()
		self.create_tables()
		self.cleanup()


	def print_trade_plans(self):
		for i, t in enumerate(self.trade_plan_array):
			if t.type != "NONE":
				print((t.type, " ",  t.amount, " at ", t.price, "$   BB: ", self.bb_scores[i- self.avg_period]))

	##simply returns name
	def get_name(self):
		return  self.NAME

	##create tables for bollinger bands as well as table for mid avg
	def create_tables(self):
		
		## create mid avg table
		pp = PointPopulator(self.candle_table_name)
		pp.setup()
		self.avg_pts = pp.create_moving_avg_simple(self.avg_period)
		##self.middle_avg_table_name = pp.create_moving_avg_simple(self.avg_period)
		##self.avg_pts = PointTable.get_point_array(self.middle_avg_table_name)
		
		##create standard deviation line
		pp = PointPopulator(self.candle_table_name)
		pp.setup()
		self.stddev_pts = pp.create_stddev(self.avg_period)
		
		for i, p in enumerate(self.candles):
			if i < self.avg_period: ##don't calculate stddev for first points since there is not enough history available
				pass
			else:
				bb_score = (p.close - self.avg_pts[i].value)/self.stddev_pts[i-self.avg_period].value
				self.bb_scores.append(bb_score)
		
		##self.stddev_table_name = pp.create_stddev(self.avg_period)
		##self.stddev_pts = PointTable.get_point_array(self.stddev_table_name)

		##create bollinger band tables
		##self.bb_low_name = self.create_bb(self.LOW)
		##self.bb_high_name = self.create_bb(self.HIGH)

		##self.bb_low_pts = PointTable.get_point_array(self.bb_low_name)
		##self.bb_high_pts = PointTable.get_point_array(self.bb_high_name)

	## return difference in terms of standard deviations between last candle value and bollinger bands
	## 0 means on avg, positive value is how many standard deviations above average, negative value is for below average
	def get_current_bb_score(self):
		last_candle_index = len(self.candles) - 1
		return self.bb_scores[last_candle_index - self.avg_period]




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

				new_pt = Point(bb_table_name, date, value)
				new_pt.save()
		dbm = DBManager.get_instance()
		dbm.save_and_close()
		return bb_table_name

	##returns true if operation is allowed
	def check_one_op(self, candle_num, type):
		if self.one_op:
			if TradePlan.is_historical_type(self.trade_plan_array, candle_num, self.ONE_OP_DELAY, type):
				return False
			else:
				return True
		else:
			return True
	
	## recalc amount based on whether stddev is set or not 
	def stddev_calc_amount(self, old_amount, candle_num):
		amount  = old_amount
		bb_mult = 1
		if self.stddev_adjust:
			bb_score = self.bb_scores[candle_num - self.avg_period]
			if bb_score > self.bb_factor:
				bb_mult = bb_score - self.bb_factor
			elif bb_score < -1*self.bb_factor:
				bb_mult = bb_score + self.bb_factor
				bb_mult *= -1
			
			amount = amount * bb_mult
		return amount

	## recalc amount based on whether carry is set or not 
	def carry_calc_amount(self, old_amount, candle_num, type):
		amount = old_amount
		if self.to_carry:
			if type == "SELL":
				amount += TradePlan.sum_past(self.trade_plan_array, candle_num, TradePlan.PLAN_SELL)
			else:
				amount += TradePlan.sum_past(self.trade_plan_array, candle_num, TradePlan.PLAN_BUY)
		return amount

	## returns true iff wait_better is turned off or bb_score has improved
	def check_wait_better(self, candle_num):
		if self.wait_better:
			if math.fabs(self.bb_scores[candle_num- self.avg_period]) < math.fabs(self.bb_scores[candle_num - self.avg_period - 1]): ##score improved
				return True
			else:
				return False
		else:
			return True


	## determines whether to sell or not and the amount 
	def validate_sell(self, candle_num, amount):
		amount = self.stddev_calc_amount(amount, candle_num)
		type = ""
		if (TradePlan.check_past(self.trade_plan_array, candle_num, self.num_past_sell, TradePlan.PLAN_SELL) or TradePlan.check_past(self.trade_plan_array, candle_num, 1, TradePlan.SELL)) and \
			self.check_one_op(candle_num, TradePlan.SELL) and \
			self.check_wait_better(candle_num):
			
			##amount = bits/10
			amount = self.carry_calc_amount(amount, candle_num, "SELL")
			type = TradePlan.SELL
		else:
			type = TradePlan.PLAN_SELL
		return (amount, type)

	## determines whether to buy or not and the amount 
	def validate_buy(self, candle_num, amount):
		amount = self.stddev_calc_amount(amount, candle_num)
		type = ""
		if TradePlan.check_past(self.trade_plan_array, candle_num, self.num_past_buy, TradePlan.PLAN_BUY) and \
			self.check_one_op(candle_num, TradePlan.BUY) and \
			self.check_wait_better(candle_num):
			amount = self.carry_calc_amount(amount, candle_num, "BUY")
			type = TradePlan.BUY
		else:
			type = TradePlan.PLAN_BUY
		return (amount, type)

	##returns market operation
	def decide(self, candle_num, bits, balance):
		date = self.candles[candle_num].date
		amount = self.amount
		price = self.candles[candle_num].close
		bb_low_val = self.avg_pts[candle_num].value - self.bb_factor*(self.stddev_pts[candle_num-self.avg_period ]).value
		bb_high_val = self.avg_pts[candle_num].value + self.bb_factor*(self.stddev_pts[candle_num-self.avg_period ]).value
		##print amount	


		##don't trade for if within first period that does not have adequate history
		if candle_num <= self.avg_period:
			type = TradePlan.NONE
		else:
			##if current price exceeds high bollinger band -> sell
			if self.bb_scores[candle_num - self.avg_period] > self.bb_factor:
				ret = self.validate_sell(candle_num, amount)
				amount = ret[0]
				type = ret[1]
			##if current price is below low bollinger band -> buy
			##if price < bb_low_val:
			elif self.bb_scores[candle_num - self.avg_period] < -1*self.bb_factor:
				ret = self.validate_buy(candle_num, amount)
				amount = ret[0]
				type = ret[1]
			##if between bollinger bands do nothing 
			else:
				type = TradePlan.NONE
		
		##print type
		self.trade_plan_array.append(TradePlan(date, amount, price, type))
		if type == TradePlan.NONE or type == TradePlan.PLAN_BUY or type == TradePlan.PLAN_SELL:
			return Operation(Operation.NONE_OP, 0)
		else:
			return Operation(type, amount)


	##set default parameters that are not set
	def set_defaults(self):
		if CandleTable.get_period(self.table_name) == "14400":
			self.bb_factor = 2.5
			self.stddev_adjust = False 
			self.avg_period = 40 
			self.num_past_buy = 0 
			self.num_past_sell = 3 
			self.one_op = False 
			self.to_carry = True 
			self.wait_better = True 
		if CandleTable.get_period(self.table_name) == "7200":
			self.bb_factor = 2
			self.stddev_adjust = False 
			self.avg_period = 80 
			self.num_past_buy = 0 
			self.num_past_sell = 6 
			self.one_op = False
			self.to_carry =False 
			self.wait_better = False 
	
	##delete tables that were created
	def cleanup(self):
		pass
		##self.dbm.drop_table(self.middle_avg_table_name)
		##self.dbm.drop_table(self.stddev_table_name)
		##self.dbm.drop_table(self.bb_low_name)
		##self.dbm.drop_table(self.bb_high_name)
		##self.dbm.save_and_close()
