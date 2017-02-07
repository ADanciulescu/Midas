##optimizes parameters of strategies
## digital optimizer
## does so by trying every possible combination of parameters and then keeping track of what combination has top performance

from bollinger_strategy import BollingerStrategy

class ParameterOptimizer:

	def __init__(self, test_tables):
		self.test_tables = test_tables

	## optimizes bollinger strategies
	## passed in default values of each parameter
	## tries parameter values around each parameter
	def optimize_bollinger(self, bb_factor = 2.5, stddev_adjust = True):
		pass
