## Model for order performed by strategy 
## attributes id, curr_pair, date_placed, date_filled, amount, rate, type

import sqlite3
from db_manager import DBManager

class Order:
	
	ID = "id"
	CURR_PAIR = "curr_pair"
	DATE_PLACED = "date_placed"
	DATE_FILLED = "date_filled"
	AMOUNT = "amount"
	RATE = "rate"
	TYPE = "type"
	BID_TYPE = "bid"
	ASK_TYPE = "ask"

	def __init__(self, table_name, id, curr_pair, date_placed, amount, rate, type, date_filled = "NULL"):
		self.id = id
		self.curr_pair = curr_pair
		self.date_placed = date_placed
		self.date_fileed = date_filled
		self.amount = amount
		self.rate = rate
		self.type = type

	##uses cursor tuple to create a Point object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Order(table_name, tup[0], tup[1], tup[2], tup[4], tup[5], tup[6], tup[3])
	
	##inserts trade into db
	def save(self):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		try:
			exec_string = "INSERT INTO {tn} ({nf_id}, {nf_curr_pair}, {nf_date_placed}, {nf_date_filled}, {nf_amount}, {nf_rate}, {nf_type}) VALUES\
					({v_id}, {v_curr_pair}, {v_date_filled}, {v_date_placed}, {v_amount}, {v_rate}, '{v_type}')"\
				.format(tn = self.table_name, nf_id = Order.ID, nf_curr_pair = Order.CURR_PAIR, nf_date_placed = Order.DATE_PLACED, nf_date_filled = Order.DATE_FILLED, nf_amount = Order.AMOUNT, nf_rate = Order.RATE, nf_type = Order.TYPE, v_id = self.id, v_curr_pair = self.curr_pair, v_date_placed = self.date_placed, v_date_filled = self.date_filled, v_amount = self.amount, v_rate = self.rate, v_type = self.type)
			cursor.execute(exec_string)
			
			db_manager.save_and_close()

		except sqlite3.IntegrityError:
			pass 
			##print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))

	##updates an already existing trade
	def update(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "UPDATE {tn} SET {nf_curr_pair} = {v_curr_pair}, {nf_date_placed} = {v_date_placed}, {nf_date_filled} = {v_date_filled}, {nf_amount} = {v_amount}, {nf_rate} = {v_rate}, {nf_type} = '{v_type}'\
					WHERE {nf_id} = {v_id}"\
				.format(tn = self.table_name, nf_curr_pair = Order.CURR_PAIR, nf_date_placed = Order.DATE_PLACED, nf_date_filled = Order.DATE_FILLED, nf_amount = Order.AMOUNT, nf_rate = Order.RATE, nf_type = Order.TYPE, v_curr_pair = self.curr_pair, v_date_placed = self.date_placed, v_date_filled = self.date_filled, v_amount = self.amount, v_rate = self.rate, v_type = self.type)
			cursor.execute(exec_string)
			dbm.save_and_close()

		except sqlite3.IntegrityError:
			print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))
