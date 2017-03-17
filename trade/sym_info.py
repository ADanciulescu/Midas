##holds information about each symbol
##info = open orders, balance etc.


class SymInfo:
	def __init__(self, sym):
		self.sym = sym
		self.available_balance = 0
		self.open_selling_amt = 0 
		self.open_buying_amt = 0
		self.total_balance = 0
		self.open_buy_orders = []
		self.open_sell_orders = []
		self.is_owned = False

	def update(self, available_balance, open_buy_orders, open_sell_orders):
		if (len(open_buy_orders) + len(open_sell_orders)) > 2:
			print("Too many open orders for:", self.sym)
		
		
		self.open_buy_orders = open_buy_orders
		self.open_sell_orders = open_sell_orders
		self.available_balance = available_balance
		self.calculate_stats()


	def calculate_stats(self):
		self.open_buying_amt = 0 
		for o in self.open_buy_orders:
			self.open_buying_amt += o.amount
		self.open_selling_amt = 0 
		for o in self.open_sell_orders:
			self.open_selling_amt += o.amount

		self.total_balance = self.open_selling_amt + self.available_balance
		if self.total_balance > 0:
			self.is_owned = True
		else:
			self.is_owned = False 
