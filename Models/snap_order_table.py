## holds orders for each snap(matched up by date)
## columns: date, amount, rate, type
from snap_order import SnapOrder
from db_manager import DBManager

class SnapOrderTable:
	

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates snap order table in db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} {nn}, {nf_amount} {ft_r} {nn}, {nf_rate} {ft_r} {nn}, {nf_type} {ft_t} {nn}, PRIMARY KEY ({nf_date}, {nf_rate}))'\
				.format(tn = self.table_name, nf_date = SnapOrder.DATE, nf_amount = SnapOrder.AMOUNT, nf_rate = SnapOrder.RATE, nf_type = SnapOrder.TYPE, ft_t = DBManager.TEXT, ft_r = DBManager.REAL, ft_i = DBManager.INTEGER, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		dbm.save_and_close()

	## returns a snap order table name from a snap table name
	@staticmethod
	def create_name(snap_table_name):
		return snap_table_name.replace("SNAP", "SNAP_ORDER")

	##returns cursor to all snap orders in table_name)
	@staticmethod
	def get_snap_order_cursor(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns snap objects for the given table_name
	@staticmethod
	def get_snap_order_array(table_name):
		##returns a cursor pointing to all snap orders linked to the table_name
		cursor = SnapOrderTable.get_snap_order_cursor(table_name)
		snap_orders = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			s = SnapOrder.from_tuple(table_name, row) 
			snap_orders.append(s)
			row = cursor.fetchone()
		return snap_orders

	##deletes all rows
	@staticmethod
	def delete_rows(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("DELETE FROM '{tn}'".format(tn = table_name))
		dbm.save_and_close()

