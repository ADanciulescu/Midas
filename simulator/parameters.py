## holds the values of particular parameter setup

class Parameters:

	def __init__(self, bb_factor, stddev_adjust, avg_period, num_past_buy, num_past_sell):
		self.bb_factor = bb_factor
		self.stddev_adjust = stddev_adjust
		self.avg_period = avg_period
		self.num_past_buy = num_past_buy
		self.num_past_sell = num_past_sell
	
	def set_balance(self, balance):
		self.balance = balance
	
	def set_percent_profit(self, pp):
		self.percent_profit = pp
							
							
	def pprint(self):
		print "bb: ", self.bb_factor, " std: ", self.stddev_adjust, " period: ", self.avg_period, " num_buy: ", self.num_past_buy, " num_sell: ", self.num_past_sell
		print "Balance: ", self.balance
		print "Percent Profit: ", self.percent_profit
