## a table containing orders on the market 
## stores market orders
## each row is an order
## columns: id, curr_pair, date_placed, date_filled, amount, rate, type
from db_manager import DBManager
from order import Order

class OrderTable:

	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates order table in db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY {nn}, {nf_curr_pair} {ft_t} {nn}, {nf_date_placed} {ft_i} {nn}, {nf_date_filled} {ft_i}, {nf_amount} {ft_r} {nn}, {nf_rate} {ft_r} {nn}, {nf_type} {ft_t})'\
				.format(tn = self.table_name, nf_id = Order.ID, nf_curr_pair = Order.CURR_PAIR, nf_date_placed = Order.DATE_PLACED, nf_date_filled = Order.DATE_FILLED, nf_amount = Order.AMOUNT, nf_rate = Order.RATE, nf_type = Order.TYPE,  ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, ft_t = DBManager.TEXT, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		dbm.save_and_close()
	
	##returns cursor to all orders in table_name)
	@staticmethod
	def get_order_cursor(table_name):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor
	
	##returns order objects for the given table_name
	@staticmethod
	def get_order_array(table_name):

		##returns a cursor pointing to all orders linked to the table_name
		cursor = OrderTable.get_order_cursor(table_name)
		orders = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			o = Order.from_tuple(table_name, row) 
			orders.append(o)
			row = cursor.fetchone()
		return orders

	@staticmethod
	def create_tables():
		ot = OrderTable(Order.ORDER_ACTIVE)
		ot.save()
		ot = OrderTable(Order.ORDER_FILLED)
		ot.save()
		ot = OrderTable(Order.ORDER_CANCELLED)
		ot.save()
