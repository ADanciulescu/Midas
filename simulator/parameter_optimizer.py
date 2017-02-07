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
		bb_vals = [2, 2.5, 3]
		std_vals = [True, False]
		period_vals = [30, 40, 50, 60]
		num_buy_vals = [0, 1]
		num_sell_vals = [0 , 1, 2, 3]

		self.parameters_array = []

		for bb in bb_vals:
			for std in std_vals:
				for period in period_vals:
					for num_buy in num_buy_vals:
						for num_sell in num_sell_vals:
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
							self.parameters_array.append(p)

		self.print_best()

	##print the paramater combination with the best balance
	def print_best(self):
		max_p = self.parameter_array[0]
		for p in self.parameter_array:
			if p.balance > max_p.balance:
				max_p = p
		
		print "Best:"
		max_p.pprint()

						




