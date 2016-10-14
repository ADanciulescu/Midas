##simulates trading of an asset using a strategy
##passed in table_name to run on and strategy to use
##prints stats about trading session

from db_manager import DBManager
from candle import Candle
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

		self.candles = []

	def run(self):
		self.candles = Candle.get_candle_array(self.table_name)
		self.strategy.cur_traded_candles = self.candles

		for i, t in enumerate(self.candles):
			operation = self.strategy.decide(i, self.bits)
			self.perform_operation(operation, t)

		self.update_net_worth()
		self.print_results()

	def print_results(self):
		print "Ended with: "
		print "Money:" + str(self.bank)
		print "Bits:" + str(self.bits)
		print "Net Worth:" + str(self.net_worth)

	## returns net_worth which is equal to money + w/e money you get by selling bits during the last candle 
	def update_net_worth(self):
		self.net_worth = self.bank
		last_price = self.candles[-1].close
		self.net_worth += self.bits*last_price

	##performs market operation updating bits and bank
	def perform_operation(self, operation, candle):
		
		amount = operation.amount
		price = candle.close
		
		if operation.op == Operation.NONE_OP or operation.amount == 0:
			pass
		elif operation.op == Operation.BUY_OP:
				print "Bought: ", self.amount
				self.bank -= amount*price
				self.bits += amount
		elif operation.op == Operation.SELL_OP:
			if self.bits > amount: ##if there are enough bits to sell
				print "Sold: ", self.amount
				self.bank += amount*price
				self.bits -= amount
			else:
				print "Sell operation failed because not enough bits are owned"
				print "Bits: " , self.bits
				print "Sold Amount Attempted: " , self.amount

		



		

