##simulates trading of an asset using a strategy
##passed in table_name to run on and strategy to use
##prints stats about trading session

from db_manager import DBManager
from candle import Candle
from candle_table import CandleTable
from test_strategy import TestStrategy
from operation import Operation
from trade_logger import TradeLogger
from trade_table import TradeTable
from trade import Trade

class TradeSimulator:

	def __init__(self, table_name, strategy):
		self.table_name = table_name
		self.strategy = strategy
	
		self.bank = 0 ##keeps track of money spent and made
		self.bits = 0 ##keeps track of bits owned
		self.total_bought = 0
		self.total_sold = 0


		self.candles = []

	def run(self):

		##create trade logger
		self.trade_table_name = TradeTable.calc_name(self.table_name, self.strategy.get_name())
		self.trade_logger = TradeLogger(self.trade_table_name, self.table_name)

		self.candles = CandleTable.get_candle_array(self.table_name)
		self.strategy.cur_traded_candles = self.candles

		for i, t in enumerate(self.candles):
			operation = self.strategy.decide(i, self.bits)
			self.process_operation(operation, t)

		self.update_net_worth()
		self.print_results()

	def print_results(self):
		print "Total Bought: ", self.total_bought
		print "Total Sold: ", self.total_sold
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
	def process_operation(self, operation, candle):
		
		amount = operation.amount
		price = candle.close
		
		if operation.op == Operation.NONE_OP or operation.amount == 0:
			pass
		elif operation.op == Operation.BUY_OP:
			self.perform_buy(candle.date, amount, price)
		elif operation.op == Operation.SELL_OP:
			if self.bits >= amount: ##if there are enough bits to sell
				self.perform_sell(candle.date, amount, price)
			else:
				print "Sell operation failed because not enough bits are owned"
				print "Bits: " , self.bits
				print "Sold Amount Attempted: " , amount
	
	def perform_buy(self, date, amount, price):
		print "Bought: " + str(amount) + " at: " + str(price)
		self.bank -= amount*price
		self.bits += amount
		self.total_bought += amount
		self.trade_logger.log_trade(date, amount, price, Trade.BUY_TYPE)
	
	def perform_sell(self, date, amount, price):
		print "Sold: " + str(amount) + " at: " + str(price)
		##print "Sold: ", amount
		self.bank += amount*price
		self.bits -= amount
		self.total_sold += amount
		self.trade_logger.log_trade(date, amount, price, Trade.SELL_TYPE)
	



		



		

