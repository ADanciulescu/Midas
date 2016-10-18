## a table containing date value pairs(points) that I generate
## can be used to visualize data and debug
## each row is a point
## columns: id, date, value
from db_manager import DBManager


class PointTable:
	
	ID = "id"
	DATE = "date"
	VALUE = "value"

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates point table in db
	def save(self):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY {nn}, {nf_date} {ft_i} {nn}, {nf_val} {ft_r} {nn})'\
				.format(tn = self.table_name, nf_id = self.ID, nf_date = self.DATE, nf_val = self.VALUE, ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, nn = DBManager.NOT_NULL)
		print exec_string
		cursor.execute(exec_string)
		db_manager.save_and_close()
	
	##returns cursor to all points in table_name)
	@staticmethod
	def get_point_cursor(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns value for given index
	@staticmethod
	def lookup(table_name, index):
		print index
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT value FROM '{tn}' WHERE id = {i}".format(tn = table_name, i = index)
		print exec_string
		cursor.execute(exec_string)
		return cursor.fetchone()


