## adapter that is created by ShortTermStrategy
##called by decide() before it returns to possibly modify trades reccomended to the simulator
from operation import Operation
from trade_simulator import TradeSimulator

class ShortStratAdapter:
	
	def __init__(self, is_simul):
		self.limit = None 
		self.curr_balance = 0
		self.is_simul = is_simul

	def set_limit(self, limit):
		self.limit = limit

	##logic to approve or disapprove a buy/sell depending on other logic i.e amount owned
	def approve(self, rate, amount, type, balance, bits):
		if type == Operation.BUY_OP:
			if bits <= 0: ##if not owned go on
				if self.limit is not None: ## limit on balance exists, make sure buy stays within limit
					allowance = balance - self.limit
					amount_allowed = allowance/(rate*(1+TradeSimulator.BUY_FEE))
					##if amount_allowed <= 0:
						##pass
					##elif bits <= 0:
						##amount_allowed = amount_allowed/3
					##elif amount_allowed/bits < 2.01 and amount_allowed/bits > 1.99:
						##amount_allowed = bits
					##elif amount_allowed/bits < 0.51 and amount_allowed/bits > 0.49:
						##amount_allowed = bits/2

					if amount_allowed > 0:
						return(amount_allowed, type)
					else:
						return (0, Operation.NONE_OP)
				else:## no limit approve operation
					return (amount, type)


			else:## if already owned disapprove buy
				return (0, Operation.NONE_OP)

		elif type == Operation.SELL_OP:
			if bits > 0:
				return (amount, type)
			else:
				return (0, Operation.NONE_OP)
	


