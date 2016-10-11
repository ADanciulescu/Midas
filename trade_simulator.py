##simulates trading of an asset using a strategy
##passed in table_name to run on and strategy to use
##prints stats about trading session

from db_manager import DBManager
from chart_tick import ChartTick
from test_strategy import TestStrategy
from operation import Operation

class TradeSimulator:

	def __init__(self, table_name, strategy):
		self.table_name = table_name
		self.strategy = strategy
	
		##keeps track of money spent and made
		self.bank = 0
		##keeps track of bits owned
		self.bits = 0

		self.ticks = []

	def run(self):
		self.ticks = self.get_tick_array()
		self.strategy.ticks = self.ticks

		for i, t in enumerate(self.ticks):
			operation = self.strategy.decide(i, self.bits)
			self.perform_operation(operation, t)

		self.update_net_worth()
		self.print_results()

	def print_results(self):
		print "Ended with: "
		print "Money:" + str(self.bank)
		print "Bits:" + str(self.bits)
		print "Net Worth:" + str(self.net_worth)

	## returns net_worth which is equal to money + w/e money you get by selling bits during the last tick
	def update_net_worth(self):
		self.net_worth = self.bank
		last_price = self.ticks[-1].close
		self.net_worth += self.bits*last_price

	##performs market operation updating bits and bank
	def perform_operation(self, operation, tick):
		
		amount = operation.amount
		price = tick.close
		
		if operation.op == Operation.NONE_OP or operation.amount == 0:
			pass
		elif operation.op == Operation.BUY_OP:
			self.bank -= amount*price
			self.bits += amount
		elif operation.op == Operation.SELL_OP:
			self.bank += amount*price
			self.bits -= amount

		
	##returns array of json entries each corresponding to a tick
	def get_tick_array(self):
		db_manager = DBManager()

		##returns a cursor pointing to all ticks linked to the table_name
		cursor = db_manager.get_tick_cursor(self.table_name)
		
		ticks = []

		##loop through cursor and add all ticks to array
		row = cursor.fetchone()
		while row is not None:
			t = ChartTick.from_tuple(self.table_name, row) 
			ticks.append(t)
			row = cursor.fetchone()
		return ticks



		

