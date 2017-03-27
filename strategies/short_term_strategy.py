## buys at the beggining and then holds the currency, used to compare to actual strategy to normalize for natural trend in currency
from operation import Operation
from candle_table import CandleTable
from trade_simulator import TradeSimulator
from interval_array import IntervalArray
from point import Point
from range import Range
from moving_average import MovingAverage
from point_table import PointTable
from db_manager import DBManager
from point_populator import PointPopulator
from strat_stat import StratStat
from strat_stat_table import StratStatTable
from standard_deviation import StandardDeviation
from short_strat_adapter import ShortStratAdapter

class ShortTermStrategy:

	NAME = "SHORTTERM"
	DATA_PAST = 25 
	VOL_PERIOD_LONG = 500
	VOL_PERIOD_SHORT = 20 
	STDDEV_PERIOD_LONG = 100 
	STDDEV_PERIOD_SHORT = 10

	def __init__(self, table_name, is_simul = True, to_print = False, calc_stats = False):
		self.table_name = table_name
		self.candles = CandleTable.get_candle_array(table_name)
		self.to_print = to_print
		self.calc_stats = calc_stats
		self.interval_array = None
		self.is_simul = is_simul
		self.area_array = []

		self.adapter = ShortStratAdapter(is_simul)

		if is_simul:
			self.amount = TradeSimulator.get_currency_amount(table_name)
		else:
			self.amount = 1
		
		init_candles = self.candles[:self.DATA_PAST]
		self.ranges = self.create_ranges(init_candles)
		self.interval_array = self.create_interval_array(self.ranges)
		
		##self.interval_array.pprint()
		##print self.interval_array.local_maxes
		##print self.interval_array.get_limits(773)
		##self.update_levels(self.ranges, self.DATA_PAST)
		sym = CandleTable.get_target_currency(table_name)

		if is_simul:
			self.calc_vol_tables()
	
	def calc_vol_tables(self):
		if self.calc_stats:
			self.strat_stat_array = []
			self.ss_tn = StratStatTable.calc_name(self.table_name, self.NAME)
			if DBManager.exists_table(self.ss_tn):
				DBManager.drop_table(self.ss_tn)
			sst = StratStatTable(self.ss_tn)
			sst.save()

		pt_name = CandleTable.to_point_table(self.table_name, "volume")
		pt_close = CandleTable.to_point_table(self.table_name, "close")
		self.points = PointTable.get_point_array(pt_name)
		self.points_close = PointTable.get_point_array(pt_close)
		pt_name_1 = "TEMP1"
		mv1 = MovingAverage(pt_name_1, self.points)
		pt_name_2 = "TEMP2"
		mv2 = MovingAverage(pt_name_2, self.points)
		self.vol_pts_short = mv1.simple(self.VOL_PERIOD_SHORT)
		self.vol_pts_long = mv2.simple(self.VOL_PERIOD_LONG)
		
		##pp = PointPopulator(self.table_name) 
		##self.stddev_pts_short = pp.create_stddev(self.STDDEV_PERIOD_SHORT) 
		##self.stddev_pts_long = pp.create_stddev(self.STDDEV_PERIOD_LONG) 
		DBManager.drop_matching_tables("TEMP")


	##called by signaler when it grabs new data
	def update_state(self, new_candles):
		self.candles = new_candles



	def create_interval_array(self, ranges):
		##insert first range
		if ranges[0].type == "DESC":
			new_range = Range(ranges[0].pt2, ranges[0].pt1, 1)
		else:
			new_range = Range(ranges[0].pt1, ranges[0].pt2, 1)

		interval_array = IntervalArray([new_range])

		for r in ranges[1:]:
			interval_array.add_range(r)
	
		interval_array.update_intervals()

		return interval_array
		##self.interval_array.pprint()
		##self.interval_array.find_local_mins()
		##print self.interval_array.local_mins
		##self.interval_array.calc_cumulative()
		##self.interval_array.find_local_maxes()
		##print self.interval_array.local_maxes
		##print self.interval_array.find_percentile(742.9959858699999, 744.10375414, 0.3)
		##print self.interval_array.area_between(742.9959858699999, 744.10375414)


	def create_ranges(self, candles):
		ranges = []
		i = 0
		while i < len(candles)-1:
			pt1 = Point("", candles[i].date, candles[i].close)
			pt2 = Point("", candles[i+1].date, candles[i+1].close)
			new_r = Range(pt1, pt2, 0)
			ranges.append(new_r)
			i += 1
		return ranges

	##def update_interval_array(self, candle_num):
		##self.interval_array.delete_range


	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits, balance):
		if candle_num < self.DATA_PAST:
			return Operation(Operation.NONE_OP, 0)
		else:
			##if called by signaler, need to recalculate interval_array
			if not self.is_simul:
				num_candles = len(self.candles)
				range_candles = self.candles[candle_num-self.DATA_PAST+1:candle_num + 1]
				self.ranges = self.create_ranges(range_candles)
				self.interval_array = self.create_interval_array(self.ranges)
	
			##make sure that more volume was traded during the next candle than amount intended to trade
			##this ensures a valid trade could have plausably happened	
			##if self.is_simul and ((candle_num == len(self.candles)-1) or self.candles[candle_num+1].volume < self.amount):
				##self.recalc_interval_array(candle_num)
				##return Operation(Operation.NONE_OP, 0)

			##if self.is_simul and candle_num != len(self.candles)-1:
				##if self.candles[candle_num+1].volume < self.amount:
					##return Operation(Operation.NONE_OP, 0)



			type = Operation.NONE_OP
			amount = 0
			
			(floor, ceiling) = self.interval_array.get_limits(self.candles[candle_num].close)
			self.floor = floor
			self.ceiling = ceiling
			##print(("f:", floor,"c:",  ceiling, "prev:", self.candles[candle_num-1].close, "cur:", self.candles[candle_num].close))	

			##if self.is_simul and candle_num > self.STDDEV_PERIOD_LONG:
				##if self.vol_pts_short[candle_num].value > self.vol_pts_long[candle_num].value:
					##self.recalc_interval_array(candle_num)
					##return Operation(Operation.NONE_OP, 0)
				##if self.vol_pts_short[candle_num].value > 0:
					##self.factor = self.vol_pts_short[candle_num].value/self.vol_pts_long[candle_num].value				
				##else:
					##self.factor = 1
				
				##self.factor = self.stddev_pts_short[candle_num-self.STDDEV_PERIOD_SHORT].value/self.stddev_pts_long[candle_num-self.STDDEV_PERIOD_LONG].value				
				##self.factor = self.stddev_pts_long[candle_num-self.STDDEV_PERIOD_LONG].value/self.stddev_pts_long[candle_num-self.STDDEV_PERIOD_LONG].value				
			##else:
				##self.factor = 1

			if floor > 0:
				self.area_array.append((floor, ceiling))

			##if broke underneath floor since last candle -> buy
			if self.candles[candle_num-1].close > floor and self.candles[candle_num].close < floor:
				type = Operation.BUY_OP
				amount = self.amount
				if self.is_simul and self.calc_stats:
					ss = StratStat(self.ss_tn, self.candles[candle_num].close, candle_num)
					self.strat_stat_array.append(ss)

				(amount, type) = self.adapter.approve(self.candles[candle_num].close, amount, type, balance, bits)
			##if broke through ceiling since last candle -> sell
			elif self.candles[candle_num-1].close < ceiling and self.candles[candle_num].close > ceiling:
				type = Operation.SELL_OP
				amount = bits 
				
				if self.is_simul and self.calc_stats:
					ss = self.strat_stat_array[-1]
					sell_rate = self.candles[candle_num].close
					total_volume = 0
					total_price = 0
					num_candles = 0
					for c in self.candles[ss.buy_candle_index:candle_num+1]:
						total_volume += c.volume
						total_price += c.close
						num_candles+=1
					stddev = StandardDeviation.simple(self.points_close[ss.buy_candle_index:candle_num+1])
					volatility = stddev/(total_price/num_candles)
					ss.update_values(sell_rate, total_volume, volatility)
					ss.save()
				(amount, type) = self.adapter.approve(self.candles[candle_num].close, amount, type, balance, bits)
			elif floor == -1:
				##if self.last == "buy":
					##if self.candles[candle_num].close < self.area_array[-1][0]:
						##type = Operation.SELL_OP
						##amount = self.amount
						##self.last = "sell"
					##else:
						##type = Operation.NONE_OP
						##amount = 0 
				##else:
					##type = Operation.NONE_OP
					##amount = 0 
				type = Operation.NONE_OP
				amount = 0 
			else:
				type = Operation.NONE_OP
		
			if self.is_simul:
				self.recalc_interval_array(candle_num)
			return Operation(type, amount)
				
	
	def recalc_interval_array(self, candle_num):
		pt1 = Point("", self.candles[candle_num-1].date, self.candles[candle_num-1].close)
		pt2 = Point("", self.candles[candle_num].date, self.candles[candle_num].close)
		new_r = Range(pt1, pt2, 0)
		self.ranges.pop(0)
		self.ranges.append(new_r)
		
		##if candle_num %10 == 0:
		self.interval_array = self.create_interval_array(self.ranges)

