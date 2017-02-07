##optimizes parameters of strategies
## digital optimizer
## does so by trying every possible combination of parameters and then keeping track of what combination has top performance

from bollinger_strategy import BollingerStrategy
from parameters import Parameters
from trade_simulator import TradeSimulator

class ParameterOptimizer:

	def __init__(self, test_table_array):
		self.test_table_array = test_table_array

	## optimizes bollinger strategies
	##does grid search for the best combination
	def optimize_bollinger(self):
		
		##values to test out
		self.bb_factor = [2, 2.5, 3]
		self.stddev_adjust = [True]
		self.avg_period = [30]
		self.num_past_buy = [0]
		self.num_past_sell = [0 , 1]
		##self.bb_factor = [2, 2.5, 3]
		##self.stddev_adjust = [True, False]
		##self.avg_period = [30, 40, 50, 60]
		##self.num_past_buy = [0, 1]
		##self.num_past_sell = [0 , 1, 2, 3]

		self.parameters_array = []

		for bb in self.bb_factor:
			for std in self.stddev_adjust:
				for period in self.avg_period:
					for num_buy in self.num_past_buy:
						for num_sell in self.num_past_sell:
							p = Parameters(bb, std, period, num_buy, num_sell)
							strat_array = []
							for tn in self.test_table_array:
								strat = BollingerStrategy(tn, bb_factor = bb, stddev_adjust = std, avg_period = period, num_past_buy = num_buy, num_past_sell = num_sell)
								strat_array.append(strat)
							trade_sim = TradeSimulator(self.test_table_array, strat_array, to_log = False)
							print "*************************************************************************************************************************"
							print "bb: ", bb, " std: ", std, " period: ", period, " num_buy: ", num_buy, " num_sell: ", num_sell
							trade_sim.run()
							print "*************************************************************************************************************************"
							
							p.set_balance(trade_sim.balance)
							p.set_percent_profit(trade_sim.profit_percent)
							self.parameters_array.append(p)

		self.print_summary("bb_factor")
	
	##print summary for a particular parameter
	def print_summary(self, parameter_attr):
		print "**********************************************************************************"
		##avgs out performance keeping parameter attr fixed and varying all possible combinations of the other parameters 
		for v in getattr(self, parameter_attr):
			total_balance = 0
			total_pp = 0
			count = 0
			for p in self.parameters_array:
				if getattr(p, parameter_attr) == v:
					total_balance += p.balance
					total_pp += p.percent_profit
					count += 1
			avg_balance = total_balance/count
			avg_pp = total_pp/count
			print parameter_attr, ": ", v
			print "Balance Avg: ", avg_balance
			print "Profit Percent Avg: ", avg_pp


		print "**********************************************************************************"
		self.print_best("balance")
		print "**********************************************************************************"
		self.print_best("percent_profit")

	##print the paramater combination with the best balance
	def print_best(self, attr):
		max_p = self.parameters_array[0]
		for p in self.parameters_array:
			if getattr(p, attr) > getattr(max_p, attr):
				max_p = p
	
		print "Best ", attr, ": "
		max_p.pprint()

						




