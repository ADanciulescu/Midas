from poloniex_client import PoloniexClient
from db_manager import DBManager
from trade_simulator import TradeSimulator
from test_strategy import TestStrategy

def main():
	get_tick_data()
	##drop_table("eth_test")

	##table_name = "USDT_BTC_1470628800_9999999999_14400"
	##table_name = "USDT_BTC_1470628800_9999999999_300"
	##simulate_test_strategy(table_name)

##drops table that matches the given table name
def drop_table(table_name):
	db_manager = DBManager()
	db_manager.drop_table(table_name)

	
def simulate_test_strategy(table_name):
	test_strat = TestStrategy()
	trade_sim = TradeSimulator(table_name, test_strat)
	trade_sim.run()

##grabs tick data from poloniex and enters it into db
##data is entered into it's own table that is uniquely defined by the configurations(currenct pair, start, end etc.)
def get_tick_data():
	##configuration
	start = 1470628800 ## aug 8 2016
	end = 9999999999 ## present
	period = 1800 ## in seconds
	currency_pair = "USDT_BTC"
	table_name = "{cp}_{s}_{e}_{p}".format(cp = currency_pair, s = start, e = end, p = period)
	print table_name	
	
	db_manager = DBManager()
	if db_manager.exists_table(table_name):
		##db_manager.drop_table(table_name)
		print "table with same configuration already exists, deleting it and rebuilding..."
		drop_table(table_name)
	db_manager.create_tick_table(table_name)
	pc = PoloniexClient(table_name)
	pc.populate_tick_db( start, end, period, currency_pair)

main()
