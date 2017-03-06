## buys at the beggining and then holds the currency, used to compare to actual strategy to normalize for natural trend in currency
from operation import Operation
from candle_table import CandleTable
from trade_simulator import TradeSimulator
from interval_array import IntervalArray
from point import Point
from range import Range

	
class ShortTermStrategy:

	NAME = "SHORTTERM"
	DATA_PAST = 150 

	def __init__(self, table_name, is_simul = True, to_print = False):
		self.table_name = table_name
		self.candles = CandleTable.get_candle_array(table_name)
		self.to_print = to_print
		self.interval_array = None
		self.is_simul = is_simul

		if is_simul:
			self.amount = TradeSimulator.get_currency_amount(table_name)
		else:
			self.amount = 1
		
		init_candles = self.candles[:self.DATA_PAST]
		self.ranges = self.create_ranges_better(init_candles)
		self.interval_array = self.create_interval_array(self.ranges)
		##self.interval_array.pprint()
		##print self.interval_array.local_maxes
		##print self.interval_array.get_limits(773)
		##self.update_levels(self.ranges, self.DATA_PAST)
		sym = CandleTable.get_target_currency(table_name)
			

	##called by signaler when it grabs new data
	def update_state(self, new_candles, is_avail):
		self.candles = new_candles
		if is_avail:
			self.last = "buy"
		else:
			self.last = "sell"



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




	##merge ranges separated by a range of period length 1
	@staticmethod
	def merge_ranges(ranges):
		merged_ranges = []
		i = 0
		while i < len(ranges):
			if i > len(ranges)-3 or ranges[i+1].get_len() != 1:
				r = ranges[i]
				i += 1
			else:
				r = Range.merge(ranges[i], ranges[i+2], 0)
				i += 3
			merged_ranges.append(r)
			
		if len(ranges) != len(merged_ranges):
			return ShortTermStrategy.merge_ranges(merged_ranges)
		else:
			return merged_ranges

			

	## populate ranges	
	def create_ranges(self, train_candles):
		range_candles = self.candles[-self.DATA_PAST:]
		self.ranges = self.create_ranges_better(init_candles)
		self.interval_array = self.create_interval_array(self.ranges)
		ranges = []
		r = Range(None, None, 0)
		i = 0
		while i < len(train_candles):
			c = train_candles[i]
			if r.pt1 is None: ##new range is being created
				r.pt1 = Point("", c.date, c.open)
			elif r.pt2 is None: ##new range was just created(pt2 is still None)
				r.pt2 = Point("", c.date, c.close)
				r.calc_type()
			else: ##range already is populated, decide whether new point continues range or a new range should be created
				if r.type == "INC":
					if c.close >= r.pt2.value: ##continue trend
						r.pt2 = Point("", c.date, c.close)
					else: ##new trend must be made
						ranges.append(r)
						r = Range(None, None, 0)
						i -= 2
				else:
					if c.close <= r.pt2.value: ##continue trend
						r.pt2 = Point("", c.date, c.close)
					else: ##new trend must be made
						ranges.append(r)
						r = Range(None, None, 0)
						i -= 2
			i += 1
		return ranges
	
	def create_ranges_better(self, candles):
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
	def decide(self, candle_num, bits):
		if candle_num < self.DATA_PAST:
			return Operation(Operation.NONE_OP, 0)
		else:

			##if called by signaler, need to recalculate interval_array
			if not self.is_simul:
				num_candles = len(self.candles)
				range_candles = self.candles[candle_num-self.DATA_PAST+1:candle_num + 1]
				self.ranges = self.create_ranges_better(range_candles)
				self.interval_array = self.create_interval_array(self.ranges)
			
			type = Operation.NONE_OP
			amount = 0
			
			(floor, ceiling) = self.interval_array.get_limits(self.candles[candle_num].close)
			print(("f:", floor,"c:",  ceiling, "prev:", self.candles[candle_num-1].close, "cur:", self.candles[candle_num].close))	
			if floor == -1:
				type = Operation.NONE_OP
			##print "Floor:", self.floor.val
			##print "Ceiling:", self.ceiling.val

			##print self.candles[candle_num].date, self.candles[candle_num].close
			##if broke underneath floor since last candle -> buy
			if self.candles[candle_num-1].close > floor and self.candles[candle_num].close < floor:
				if self.last == "sell":
					type = Operation.BUY_OP
					amount = self.amount
					self.last = "buy"
			##if broke through ceiling since last candle -> sell
			elif self.candles[candle_num-1].close < ceiling and self.candles[candle_num].close > ceiling:
				if self.last == "buy":
					type = Operation.SELL_OP
					amount = self.amount
					self.last = "sell"
			else:
				##print "None"
				type = Operation.NONE_OP
		
			if self.is_simul:
				pt1 = Point("", self.candles[candle_num-1].date, self.candles[candle_num-1].close)
				pt2 = Point("", self.candles[candle_num].date, self.candles[candle_num].close)
				new_r = Range(pt1, pt2, 0)
				self.ranges.pop(0)
				self.ranges.append(new_r)
				
				##if candle_num %10 == 0:
				self.interval_array = self.create_interval_array(self.ranges)

			return Operation(type, amount)
				


