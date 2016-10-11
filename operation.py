## returned by strategy
## hold information about the market operation recommended by strategy

class Operation:
	
	BUY_OP = "BUY"
	SELL_OP = "SELL"
	NONE_OP = "NONE"

	##op = 'BUY' or 'SELL' or 'NONE'
	def __init__(self, op, amount):
		self.op = op
		self.amount = amount
