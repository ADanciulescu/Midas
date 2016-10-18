## a table containing date , # of hits for each day of google trends 
## columns: date, hits
from db_manager import DBManager


class TrendTable:
	
	DATE = "date"
	HITS = "hits"

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates trends table in db
	def save(self):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} PRIMARY KEY {nn}, {nf_hits} {ft_i} {nn})'\
				.format(tn = self.table_name, nf_date = self.DATE, nf_hits = self.HITS, ft_i = DBManager.INTEGER, ft_t = DBManager.TEXT, nn = DBManager.NOT_NULL)
		print exec_string
		cursor.execute(exec_string)
		db_manager.save_and_close()
	
	##returns cursor to all points in table_name)
	@staticmethod
	def get_trend_cursor(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor

	## returns cursor to points between the 2 dates
	@staticmethod
	def get_section(table_name, date_start, date_end):
		dbm = DBManager()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}' WHERE date > {ds} AND date < {de}".format(tn = table_name, ds = date_start, de = date_end))
		return cursor
	
