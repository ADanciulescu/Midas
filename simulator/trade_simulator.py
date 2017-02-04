##simulates trading of an asset using a strategy
##passed in table_name to run on and strategy to use
##prints stats about trading session

import time
from db_manager import DBManager
from candle import Candle
from candle_table import CandleTable
from test_strategy import TestStrategy
from operation import Operation
from trade_logger import TradeLogger
from trade_table import TradeTable
from trade import Trade
from results_logger import ResultsLogger

class TradeSimulator:

	SUPPRESS_PRINT_HISTORY = True
	##poloniex fees
	SELL_FEE = 0.0015
	BUY_FEE = 0.0025

	def __init__(self, table_name, candles, strategy):
		self.table_name = table_name
		self.strategy = strategy
	
		self.bits = 0 ##keeps track of bits owned
		self.bits_at_end = 0 ##keeps track of bits owned when algorithm ends(before they are all finally sold)
		self.total_bought = 0 ##total bits ever bought
		self.total_sold = 0 ## total bits ever sold 
		self.balance = 0 ##money balance
		self.max_debt = 0 ##lowest balance ever incurred
		self.money_spent = 0 ##total money spent
		self.candles = candles

	def run(self):

		##create results logger
		currency = CandleTable.get_target_currency(self.table_name)
		start_time = CandleTable.get_start_time(self.table_name)
		end_time = time.time() 
		##self.results_logger = ResultsLogger(currency, self.table_name, self.strategy.trends_table_name, start_time, end_time, self.strategy.AVG_SHORT_DAYS, self.strategy.AVG_LONG_DAYS)

		##create trade logger
		self.trade_table_name = TradeTable.calc_name(self.table_name, self.strategy.get_name())
		self.trade_logger = TradeLogger(self.trade_table_name, self.table_name)
		self.strategy.trade_table_name = self.trade_table_name
		

		for i, t in enumerate(self.candles):
			operation = self.strategy.decide(i, self.bits)
			self.process_operation(operation, t)

		self.finalize_balance()
		self.print_results()
		##self.log_results()

	def print_results(self):

		if not self.SUPPRESS_PRINT_HISTORY:
			print "History: "
			TradeTable.pprint(self.trade_table_name)

		##last price that any unsold bits are finally sold
		last_price = self.candles[-1].close
	
		print ""
		print "Total Bits Bought: ", self.total_bought
		print "Total Spent: ", self.money_spent
		print "Max Debt: ", self.max_debt
		##print "Total Sold: ", self.total_sold
		##print "Ended with: "
		print "Bits at end:" + str(self.bits_at_end)
		print "Final Price: ",  last_price 
		print "Balance:" + str(self.balance)
		if self.money_spent > 0:
			print "Profit Percent: " + str(self.balance/(-1*self.max_debt))
		else:
			print "NO MONEY SPENT"

	def log_results(self):
		self.results_logger.log(self.total_bought, self.money_spent, self.total_sold, self.balance, self.bits)


	## returns balance which is equal to money + w/e money you get by selling bits during the last candle 
	def finalize_balance(self):
		if self.bits > 0:
			self.bits_at_end = self.bits
			last_date = self.candles[-1].date
			last_price = self.candles[-1].close
			self.perform_sell(last_date, self.bits, last_price)

	##performs market operation updating bits and balance 
	def process_operation(self, operation, candle):
		
		amount = operation.amount
		price = candle.close
		
		if operation.op == Operation.NONE_OP or operation.amount == 0:
			pass
			##print "Nothing at: ", str(price)
		elif operation.op == Operation.BUY_OP:
			self.perform_buy(candle.date, amount, price)
		elif operation.op == Operation.SELL_OP:
			if self.bits >= amount: ##if there are enough bits to sell
				self.perform_sell(candle.date, amount, price)
			elif self.bits == 0:
				self.fail_sell(candle.date, amount, price)
			elif self.bits < amount:
				amount = self.bits
				self.perform_sell(candle.date, amount, price)

	
	def perform_buy(self, date, amount, price):
		cost = amount*price
		self.balance -= cost 
		self.balance -= cost * TradeSimulator.BUY_FEE 
		self.money_spent += cost 
		self.money_spent += cost * TradeSimulator.BUY_FEE 
		self.bits += amount
		self.total_bought += amount
		if self.balance < self.max_debt:
			self.max_debt = self.balance
		
		
		self.trade_logger.log_trade(date, amount, price, Trade.BUY_TYPE)
	
	def perform_sell(self, date, amount, price):
		cost = amount*price
		self.balance += amount*price
		self.balance -= cost * TradeSimulator.SELL_FEE
		self.bits -= amount
		self.total_sold += amount
		
		self.trade_logger.log_trade(date, amount, price, Trade.SELL_TYPE)
	
	def fail_sell(self, date, amount, price):	
		self.trade_logger.log_trade(date, amount, price, Trade.FAIL_SELL_TYPE)


		



		

