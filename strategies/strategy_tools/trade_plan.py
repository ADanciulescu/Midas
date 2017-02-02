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

	## return true if the previous num_past tadeplans before the index are of the past
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
