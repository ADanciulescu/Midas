## holds snapshots of currency order book at a certain dates
## a table containing dates that each link up to a snap_orders 
## columns: date
from snap import Snap
from db_manager import DBManager

class SnapTable:
	

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates snap table in db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} PRIMARY KEY {nn})'\
				.format(tn = self.table_name, nf_date = Snap.DATE, ft_i = DBManager.INTEGER, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		dbm.save_and_close()
	
	##returns cursor to all snaps in table_name)
	@staticmethod
	def get_snap_cursor(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns snap objects for the given table_name
	@staticmethod
	def get_snap_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = SnapTable.get_snap_cursor(table_name)
		snaps = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			s = Snap.from_tuple(table_name, row) 
			snaps.append(s)
			row = cursor.fetchone()
		return snaps

	##return currency pair from table name
	@staticmethod
	def get_currency_pair(tn):
		components = tn.split("_")
		ref_curr = components[1]
		target_curr = components[2]
		return ref_curr + "_" + target_curr
	
	##deletes all rows
	@staticmethod
	def delete_rows(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("DELETE FROM '{tn}'".format(tn = table_name))
		dbm.save_and_close()
