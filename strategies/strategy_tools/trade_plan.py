## array of these is saved by strategies so that state/history can be saved 
## attributes:  date, amount, price, type

class TradePlan:
	
	BUY = "BUY"
	SELL = "SELL"
	NONE = "NONE"
	PLAN_BUY = "PLAN_BUY"
	PLAN_SELL = "PLAN_SELL"

	def __init__(self, date, amount, price, type):
		self.date = date
		self.amount = amount
		self.price = price
		self.type = type

	##returns true if a tradeplan in the last num_past has the same type as type
	@staticmethod
	def is_historical_type(trade_plan_array, index, num_past, type):
		if len(trade_plan_array) < num_past:
			return False
		for i in range(index- num_past, index):
			if trade_plan_array[i].type == type:
				return True
			else:
				pass
		return False
	
	## return true if the previous num_past trade plans before the index are of the type given
	## otherwise return false
	@staticmethod
	def check_past(trade_plan_array, index, num_past, type):
		if len(trade_plan_array) < num_past:
			return False
		for i in range(index- num_past, index):
			if trade_plan_array[i].type == type:
				pass
			else:
				return False
		return True
	
	##return sum of amounts in all consecutive trade_plans in past that have the passed in type
	@staticmethod
	def sum_past(trade_plan_array, index, type):
		i = index - 1
		sum = 0
		while(trade_plan_array[i].type == type):
			sum += trade_plan_array[i].amount
			i -= 1
		return sum
