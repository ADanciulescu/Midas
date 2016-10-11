from poloniex_client import PoloniexClient
from db_manager import DBManager

def main():
	get_candle_data()
	##drop_table("eth_test")

##drops table that matches the given table name
def drop_table(table_name):
	db_manager = DBManager()
	db_manager.drop_table(table_name)

		
##grabs candle data from poloniex and enters it into db
##data is entered into it's own table that is uniquely defined by the configurations(currenct pair, start, end etc.)
def get_candle_data():
	##configuration
	start = 1470628800 ## aug 8 2016
	end = 9999999999 ## present
	period = 14400 ## in seconds
	currency_pair = "USDT_BTC"
	table_name = "{cp}_{s}_{e}_{p}".format(cp = currency_pair, s = start, e = end, p = period)
	
	
	db_manager = DBManager()
	if db_manager.exists_table(table_name):
		##db_manager.drop_table(table_name)
		print "table with same configuration already exists, deleting it and rebuilding..."
		drop_table(table_name)
	db_manager.create_data_table(table_name)
	pc = PoloniexClient(table_name, start, end, period, currency_pair)
	pc.run()

main()
