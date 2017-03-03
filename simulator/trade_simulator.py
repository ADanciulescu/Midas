##simulates trading of an asset using a strategy
##passed in table_name to run on and strategy to use
##prints stats about trading session

import time
from db_manager import DBManager
from candle import Candle
from candle_table import CandleTable
from operation import Operation
from trade_table import TradeTable
from trade import Trade
from results_logger import ResultsLogger

class TradeSimulator:

	##poloniex fees
	SELL_FEE = 0.0015
	BUY_FEE = 0.0025

	##core amounts for each currency
	BTC_AMOUNT = 1
	ETH_AMOUNT = 80
	XMR_AMOUNT = 70
	XRP_AMOUNT = 3000
	ETC_AMOUNT = 300
	LTC_AMOUNT = 100
	DASH_AMOUNT = 10
	REP_AMOUNT = 30
	STR_AMOUNT = 3000
	ZEC_AMOUNT = 3
	DEFAULT_AMOUNT = 10

	def __init__(self, table_name_array, strategy_array, limit = -12345, to_print = True, to_print_trades = False, to_log = True):
		self.table_name_array = table_name_array
		self.strategy_array = strategy_array
		self.balance_limit = limit ##limits how low max_debt can go before buying fails
		self.to_print = to_print
		self.to_print_trades = to_print_trades
		self.to_log = to_log
				
		self.num_currencies = len(table_name_array)
		self.symbol_array = [] ##array of symbols where each symbol signifies current for example BTC, ETH ...
		self.last_price_array = [] ##array of the last price of a bit of each currency
		self.bits_array = [] ##keeps track of bits owned
		self.bits_end_array = [] ##keeps track of bits owned when algorithm ends(before they are all finally sold)
		self.trade_table_name_array = [] ## array of trade_table_names, one for each candle table
		self.trades_array = [] ## array containing arrays of trades
		self.balance = 0 ##money balance
		self.max_debt = 0 ##lowest balance ever incurred
		self.money_spent = 0 ##total money spent
		self.bit_sec = 0 ##corresponds to the sum of bit*time held for the trading period
		self.total_bits_bought_array = [] ##holds total bits bought for each currency

		self.preprocess()

	##create neccesary data structures before simulator actually runs
	def preprocess(self):
	
		##initilize all bits to 0, get symbols
		for tn in self.table_name_array:
			self.bits_array.append(0)
			self.bits_end_array.append(0)
			self.symbol_array.append(CandleTable.get_target_currency(tn))
			self.total_bits_bought_array.append(0)

		##get candle arrays
		self.candles_array = []
		for tn in self.table_name_array:
			candles = CandleTable.get_candle_array(tn)
			self.candles_array.append(candles)
		


		##create trade tables 
		if self.to_log:
			for i, tn in enumerate(self.table_name_array):
				trade_table_name = TradeTable.calc_name(tn, self.strategy_array[i].get_name())
				trade_table = TradeTable(trade_table_name)
				if DBManager.exists_table(trade_table_name):
					DBManager.drop_table(trade_table_name)
				trade_table.save()
				self.trade_table_name_array.append(trade_table_name)
				
				self.strategy_array[i].trade_table_name = trade_table_name
				self.trades_array.append([])

	##returns index of the most candle_table
	def most_candles_index(self):
		max_len = 0
		max_index = 0 
		for i, ca in enumerate(self.candles_array):
			ca_len = len(ca)
			if max_len < ca_len:
				max_len = ca_len
				max_index = i
		return max_index
	


	def run(self):

		## first iterate over candle index
		most_candles = self.candles_array[self.most_candles_index()]
		num_most_candles = len(most_candles)
		for i in range(num_most_candles):
			##then iterate over candle table
			for j in range(self.num_currencies):
				period = CandleTable.get_period(self.table_name_array[j])
				self.bit_sec += self.bits_array[j]*int(period)
				##offset adjusts for different tables having different num of candles
				offset = num_most_candles - len(self.candles_array[j])
				if offset <= i:
					
					operation = self.strategy_array[j].decide(i - offset, self.bits_array[j])
					self.process_operation(j, operation, self.candles_array[j][i-offset])
				else: ##too early to trade these candles
					pass

		self.finalize_balance()
		
		if self.to_log:
			self.save_all_trades()
		
		if self.to_print:
			self.print_results()

	def print_results(self):
		
		if self.to_print_trades:
			for i in range(self.num_currencies):
				print "*************************************************************************************************************************"
				print "History: ", self.table_name_array[i]
				print ""
				TradeTable.pprint(self.trade_table_name_array[i])
				print "*************************************************************************************************************************"

	
		print ""
		print "Total Spent: ", self.money_spent
		print "Max Debt: ", self.max_debt
		bits_summary = self.get_bits_summary()
		print "Bits at end: ", bits_summary 
		print "Balance:" + str(self.balance)
		if self.money_spent > 0:
			print "Profit Percent: ", self.profit_percent 
		else:
			print "NO MONEY SPENT"
		##if self.num_currencies == 1:
			##self.profit_per_bitsec = self.profit_percent/self.bit_sec
			##print self.profit_per_bitsec
		print ""

	##returns snapshot at the end
	def get_bits_summary(self):
		ret_str = ""
		for i, sym in enumerate(self.symbol_array):
			if self.bits_end_array[i] > 0:
				sym_str = "(" + sym + " " + str(self.bits_end_array[i]) + " at " + str(self.last_price_array[i])  + ")"
				ret_str += sym_str
		return ret_str

	##def log_results(self):
		##self.results_logger.log(self.total_bought, self.money_spent, self.total_sold, self.balance, self.bits)


	## returns balance which is equal to money + w/e money you get by selling bits during the last candle 
	def finalize_balance(self):

		for i in range(self.num_currencies):
			last_price = self.candles_array[i][-1].close 
			self.last_price_array.append(last_price)
			last_date = self.candles_array[i][-1].date 
			self.bits_end_array[i] = self.bits_array[i]
			if self.bits_array[i] > 0:
				self.attempt_sell(i, last_date, self.bits_array[i], last_price)
		
		if self.money_spent > 0:
			self.profit_percent = self.balance/(-1*self.max_debt)
		else:
			self.profit_percent = 0

	##performs market operation updating bits and balance 
	def process_operation(self, currency_index, operation, candle):
		amount = operation.amount
		price = candle.close
		date = candle.date
		
		if operation.op == Operation.NONE_OP or operation.amount == 0:
			self.log_trade(currency_index, date, amount, price, Trade.NONE_TYPE)
		elif operation.op == Operation.BUY_OP:
			self.attempt_buy(currency_index, candle.date, amount, price)
		elif operation.op == Operation.SELL_OP:
			self.attempt_sell(currency_index, candle.date, amount, price)

	
	def attempt_buy(self, currency_index, date, amount, price):
		total_cost = (amount*price)*(1+TradeSimulator.BUY_FEE)
		allowance =  self.balance - self.balance_limit ##balance_limit is a negative number

		## if performing buy would surpass limit
		if total_cost > allowance and self.balance_limit != -12345:
			if allowance <= 0:
				self.fail_buy(currency_index, date, amount, price)
			else:
				##use all existing allowance to complete a smaller but valid buy
				new_amount = allowance/(price* (1 + TradeSimulator.BUY_FEE))
				self.attempt_buy(currency_index, date, new_amount, price)
		else: ##buying is valid, doesn't surpass limit
			self.balance -= total_cost 
			self.money_spent += total_cost 
			self.bits_array[currency_index] += amount
			self.total_bits_bought_array[currency_index] += amount
			#update max_debt
			if self.balance < self.max_debt:
				self.max_debt = self.balance
		
		
		self.log_trade(currency_index, date, amount, price, Trade.BUY_TYPE)
	
	def attempt_sell(self, currency_index, date, amount, price):
		bits = self.bits_array[currency_index]
		
		##if there are enough bits to sell
		if  bits < amount:
			if bits <= 0:
				self.fail_sell(currency_index, date, amount, price)
			else:
				##perform smaller but valid sell
				new_amount = bits
				self.attempt_sell(currency_index, date, bits, price)
		
		elif bits >= amount: ##sell is valid
			cost = amount*price
			self.balance += cost
			self.balance -= cost * TradeSimulator.SELL_FEE
			self.bits_array[currency_index] -= amount
			
			self.log_trade(currency_index, date, amount, price, Trade.SELL_TYPE)
	
	def fail_sell(self, currency_index, date, amount, price):	
		self.log_trade(currency_index, date, amount, price, Trade.FAIL_SELL_TYPE)


	def fail_buy(self, currency_index, date, amount, price):	
		self.log_trade(currency_index, date, amount, price, Trade.FAIL_BUY_TYPE)
		
	##creates a trade and adds it to the appropriate array of trades
	def log_trade(self, currency_index, date, amount, price , type):
		if self.to_log:
			t = Trade(self.trade_table_name_array[currency_index], date, amount, price, type)
			self.trades_array[currency_index].append(t)	

	def save_all_trades(self):
		for ta in self.trades_array:
			for t in ta:
				t.save()
		dbm = DBManager.get_instance()
		dbm.save_and_close()

	##returns core amount of bits to trade based on table name
	@staticmethod
	def get_currency_amount(tn):
		if "BTC" in tn:
			return TradeSimulator.BTC_AMOUNT
		elif "ETH" in tn:
			return TradeSimulator.ETH_AMOUNT
		elif "XMR" in tn:
			return TradeSimulator.XMR_AMOUNT
		elif "XRP" in tn:
			return TradeSimulator.XRP_AMOUNT
		elif "ETC" in tn:
			return TradeSimulator.ETC_AMOUNT
		elif "LTC" in tn:
			return TradeSimulator.LTC_AMOUNT
		elif "DASH" in tn:
			return TradeSimulator.DASH_AMOUNT
		elif "REP" in tn:
			return TradeSimulator.REP_AMOUNT
		elif "STR" in tn:
			return TradeSimulator.STR_AMOUNT
		elif "ZEC" in tn:
			return TradeSimulator.ZEC_AMOUNT
		else:
			return TradeSimulator.DEFAULT_AMOUNT
