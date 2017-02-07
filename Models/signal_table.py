## a table containing signals generated
## each row is a signal

from db_manager import DBManager
from sig import Sig

class SignalTable:
	
	def __init__(self, table_name):
		self.table_name = table_name
	
	##creates point table in db
	def save(self):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} PRIMARY KEY {nn}, {nf_amount} {ft_r} {nn}, {nf_price} {ft_r} {nn}, {nf_type} {ft_t} {nn})'\
				.format(tn = self.table_name, nf_date = Sig.DATE, nf_amount = Sig.AMOUNT, nf_price = Sig.PRICE, nf_type = Sig.TYPE,
						ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, ft_t = DBManager.TEXT, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		db_manager.save_and_close()
	
	##returns cursor to all signals in table_name
	@staticmethod
	def get_signal_cursor(table_name):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns signal objects for the given table_name
	@staticmethod
	def get_signal_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = SignalTable.get_signal_cursor(table_name)
		signalss = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			s= Sig.from_tuple(table_name, row) 
			signals.append(t)
			row = cursor.fetchone()
		return signals 
