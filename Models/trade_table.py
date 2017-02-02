## a table containing trades 
## can be used to visualize trades and debug
## each row is a trade
## columns: id, date, amount, price, type
from db_manager import DBManager
from trade import Trade
from candle_table import CandleTable

class TradeTable:
	

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates trade table in db
	def save(self):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} PRIMARY KEY {nn}, {nf_amount} {ft_r} {nn}, {nf_price} {ft_r} {nn}, {nf_type} {ft_t})'\
				.format(tn = self.table_name, nf_date = Trade.DATE,nf_amount = Trade.AMOUNT, nf_price = Trade.PRICE, nf_type = Trade.TYPE,  ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, ft_t = DBManager.TEXT, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		db_manager.save_and_close()
	
	##returns cursor to all trades in table_name)
	@staticmethod
	def get_trade_cursor(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns trade objects for the given table_name
	@staticmethod
	def get_trade_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = TradeTable.get_trade_cursor(table_name)
		trades = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Trade.from_tuple(table_name, row) 
			trades.append(t)
			row = cursor.fetchone()
		return trades
	
	##returns trade object for given index
	@staticmethod
	def lookup(table_name, index):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT * FROM '{tn}' WHERE id = {i}".format(tn = table_name, i = index)
		cursor.execute(exec_string)
		return Trade.from_tuple(table_name, cursor.fetchone())
	
	##returns name for trade table
	@staticmethod
	def calc_name(candle_table_name, strategy_name):
		return "TRADE_"+ strategy_name + "_" + CandleTable.get_target_currency(candle_table_name) + "_" + CandleTable.get_period(candle_table_name)

	##returns trade object for given date
	@staticmethod
	def get_trade(table_name, date):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT * FROM '{tn}' WHERE date = {d}".format(tn = table_name, d = date)
		cursor.execute(exec_string)
		return Trade.from_tuple(table_name, cursor.fetchone())
	
	##returns trade objects for given date
	@staticmethod
	def get_trades_in_range(table_name, date_low, date_high, type):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT * FROM '{tn}' WHERE date >= {d_low} AND date <= {d_high} AND type = '{t}'".format(tn = table_name, d_low = date_low, d_high = date_high, t = type)
		cursor.execute(exec_string)
		trades = []
		
		t = cursor.fetchone()
		while t is not None:
			trade = Trade.from_tuple(table_name, t)
			trades.append(trade)
			t = cursor.fetchone()
		return trades
		
	##print trade table
	@staticmethod
	def pprint(table_name):
		arr = TradeTable.get_trade_array(table_name)
		
		##count how many none operations in a row to compress the results printed
		none_counter = 0
		for t in arr:
			if t.type != Trade.NONE_TYPE:
				if none_counter > 0:
					print "***************************No operation for ticks: ", none_counter, " *************************************"
					none_counter = 0
			else:
				none_counter += 1
			t.pprint()
		print "***************************No operation for ticks: ", none_counter, " *************************************"

