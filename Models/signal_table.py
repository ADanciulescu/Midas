## a table containing signals generated
## each row is a signal

from db_manager import DBManager
from sig import Sig

class SignalTable:
	
	def __init__(self, table_name):
		self.table_name = table_name
	
	##creates point table in db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} PRIMARY KEY {nn}, {nf_sym} {ft_t} {nn}, {nf_amount} {ft_r} {nn}, {nf_price} {ft_r} {nn}, {nf_type} {ft_t} {nn})'\
				.format(tn = self.table_name, nf_date = Sig.DATE, nf_sym = Sig.SYM, nf_amount = Sig.AMOUNT, nf_price = Sig.PRICE, nf_type = Sig.TYPE,
						ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, ft_t = DBManager.TEXT, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		dbm.save_and_close()
	
	##returns cursor to all signals in table_name
	@staticmethod
	def get_signal_cursor(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns signal objects for the given table_name
	@staticmethod
	def get_signal_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = SignalTable.get_signal_cursor(table_name)
		signals = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			s = Sig.from_tuple(table_name, row) 
			signals.append(s)
			row = cursor.fetchone()
		return signals 
	
	## return date of last signal entry in the table
	@staticmethod
	def get_last_date(table_name):
		if DBManager.exists_table(table_name):
			dbm = DBManager.get_instance()
			cursor = dbm.get_cursor()
			cursor.execute(" SELECT date FROM '{tn}' WHERE date = ( SELECT MAX(date) FROM '{tn}' )".format(tn = table_name))
			return cursor.fetchone()[0]
		else:
			return 0
	
	##returns last signal in table
	@staticmethod
	def get_last_signal(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute(" SELECT * FROM '{tn}' WHERE date = ( SELECT MAX(date) FROM '{tn}' )".format(tn = table_name))
		row = cursor.fetchone()
		s = Sig.from_tuple(table_name, row)
		return s

	##return currency symbol for this signal table
	@staticmethod
	def get_sym(table_name):
		info = table_name.split("_")
		return info[3]
