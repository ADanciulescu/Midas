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
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_t} PRIMARY KEY {nn}, {nf_hits} {ft_i} {nn})'\
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
	
