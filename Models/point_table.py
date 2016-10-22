## a table containing date value pairs(points) that I generate
## can be used to visualize data and debug
## each row is a point
## columns: id, date, value
from db_manager import DBManager
from point import Point

class PointTable:
	

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates point table in db
	def save(self):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY {nn}, {nf_date} {ft_i} {nn}, {nf_val} {ft_r} {nn})'\
				.format(tn = self.table_name, nf_id = Point.ID, nf_date = Point.DATE, nf_val = Point.VALUE, ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, nn = DBManager.NOT_NULL)
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
	
	##returns point objects for the given table_name
	@staticmethod
	def get_point_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = self.get_point_cursor(table_name)
		points = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Point.from_tuple(table_name, row) 
			points.append(t)
			row = cursor.fetchone()
		return points
	
	##returns point object for given index
	@staticmethod
	def lookup(table_name, index):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT * FROM '{tn}' WHERE id = {i}".format(tn = table_name, i = index)
		cursor.execute(exec_string)
		return Point.from_tuple(table_name, cursor.fetchone())

	##returns point object for given date or the first one after
	@staticmethod
	def lookup_date(table_name, date):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT * FROM '{tn}' WHERE date <= {d}".format(tn = table_name, d = date)
		cursor.execute(exec_string)
		return Point.from_tuple(table_name, cursor.fetchone())


