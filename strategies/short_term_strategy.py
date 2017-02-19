## buys at the beggining and then holds the currency, used to compare to actual strategy to normalize for natural trend in currency
from operation import Operation
from candle_table import CandleTable
from trade_simulator import TradeSimulator
from point import Point
from range import Range
from level import Level

	
class ShortTermStrategy:

	NAME = "SHORT_TERM"
	PROP = 0.5
	REDUC_ACCEPT = 0.3

	def __init__(self, table_name, is_simul = True):
		self.candles = CandleTable.get_candle_array(table_name)
		self.train_candles = self.candles[:int(self.PROP*len(self.candles))]
		self.last_train_date = self.train_candles[-1].date


		if is_simul:
			self.amount = TradeSimulator.get_currency_amount(table_name)
		else:
			self.amount = 1
		
		self.ranges = []
		self.create_ranges()
		##self.ranges = ShortTermStrategy.merge_ranges(self.ranges)
		self.process_range()

		##for r in self.ranges:
			##r.pprint()

	def process_range(self):
		ranges = self.ranges
		##ranges = self.ranges[len(self.ranges)/20:len(self.ranges)*2/20]
		
		##find max and min reached during the ranges
		max = 0
		min = 99999999999
		for r in ranges:
			if r.type == "INC":
				if r.pt2.value > max:
					max = r.pt2.value
			if r.type == "DESC":
				if r.pt2.value < min:
					min = r.pt2.value
		inc_amt = (max - min)/100
		level_val = min
		levels = []
		while level_val < max:
			levels.append(Level(level_val, []))
			level_val+= inc_amt

		for r in ranges:
			for l in levels:
				if r.is_between(l.val):
					l.ranges.append(r)
		
		for l in levels:
			l.update_stats()
			##l.pprint()
		
		middle_level = levels[0]
		middle_i = 0
		for i, l in enumerate(levels):
			if l.total > middle_level.total:
				middle_level = l
				middle_i = i

		floor_level = middle_level
		middle_total = middle_level.total
			
		for i in range(middle_i, -1, -1):
			if levels[i].total < self.REDUC_ACCEPT*middle_total:
				floor_level = levels[i+1]
				break

		ceiling_level = middle_level 
		for i in range(middle_i, len(levels)):
			if levels[i].total < self.REDUC_ACCEPT*middle_total:
				ceiling_level = levels[i-1]
				break

		self.ceiling = ceiling_level
		self.floor = floor_level
		
		##print "Floor: "
		##self.floor.pprint()
		##print "Middle: "
		##middle_level.pprint()
		##print "Ceiling: "
		##self.ceiling.pprint()


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
				r = Range.merge(ranges[i], ranges[i+2])
				i += 3
			merged_ranges.append(r)
			
		if len(ranges) != len(merged_ranges):
			return ShortTermStrategy.merge_ranges(merged_ranges)
		else:
			return merged_ranges

			

	## populate ranges	
	def create_ranges(self):
		r = Range(None, None)
		i = 0
		while i < len(self.train_candles):
			c = self.train_candles[i]
			if r.pt1 is None: ##new range is being created
				r.pt1 = Point("", c.date, c.close)
			elif r.pt2 is None: ##new range was just created(pt2 is still None)
				r.pt2 = Point("", c.date, c.close)
				r.calc_type()
			else: ##range already is populated, decide whether new point continues range or a new range should be created
				if r.type == "INC":
					if c.close >= r.pt2.value: ##continue trend
						r.pt2 = Point("", c.date, c.close)
					else: ##new trend must be made
						self.ranges.append(r)
						r = Range(None, None)
						i -= 2
				else:
					if c.close <= r.pt2.value: ##continue trend
						r.pt2 = Point("", c.date, c.close)
					else: ##new trend must be made
						self.ranges.append(r)
						r = Range(None, None)
						i -= 2
			i += 1
			

	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits):
		date = self.candles[candle_num].date

		if date <= self.last_train_date:
			return Operation(Operation.NONE_OP, 0)
		else:
			##print self.candles[candle_num].date, self.candles[candle_num].close
			##if broke underneath floor since last candle -> buy
			##if self.candles[candle_num-1].close > self.floor.val and self.candles[candle_num].close < self.floor.val:
				##print "Bought"
				##return Operation(Operation.BUY_OP, self.amount)
			##if broke through ceiling since last candle -> sell
			##elif self.candles[candle_num-1].close < self.ceiling.val and self.candles[candle_num].close > self.ceiling.val:
				##print "Sold"
				##return Operation(Operation.SELL_OP, self.amount)
			##else:
				##return Operation(Operation.NONE_OP, 0)
			
			if self.candles[candle_num].close < self.floor.val:
				##print "Bought"
				return Operation(Operation.BUY_OP, self.amount)
			##if broke through ceiling since last candle -> sell
			elif self.candles[candle_num].close > self.ceiling.val:
				##print "Sold"
				return Operation(Operation.SELL_OP, self.amount)
			else:
				return Operation(Operation.NONE_OP, 0)


