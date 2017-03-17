## Model for order performed by strategy 
## attributes id, curr_pair, date_placed, date_filled, amount, rate, type

import sqlite3
from db_manager import DBManager
from poloniex import Poloniex
from time import time

class Order:
	##TODO: handle partially filled orders	
	ORDER_ACTIVE = "ORDER_ACTIVE"
	ORDER_FILLED = "ORDER_FILLED"
	ORDER_CANCELLED = "ORDER_CANCELLED"

	ID = "id"
	CURR_PAIR = "curr_pair"
	DATE_PLACED = "date_placed"
	DATE_FILLED = "date_filled"
	AMOUNT = "amount"
	RATE = "rate"
	TYPE = "type"
	BID = "buy"
	ASK = "sell"

	def __init__(self, table_name, id, curr_pair, date_placed, amount, rate, type, date_filled = "NULL"):
		self.table_name = table_name
		self.id = id
		self.curr_pair = curr_pair
		self.date_placed = date_placed
		self.date_filled = date_filled
		self.amount = amount
		self.rate = rate
		self.type = type

	def get_sym(self):
		return self.curr_pair.split("_")[1]

	##uses cursor tuple to create a Point object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Order(table_name, tup[0], tup[1], tup[2], tup[4], tup[5], tup[6], tup[3])


	## update the order based on orderbook from poloniex
	def polo_update(self):
		polo = Poloniex.get_instance()
		polo_data = polo.api_query("returnOpenOrders", {'currencyPair': self.curr_pair})
		if polo_data is None:
			print("API error unable to polo_update order")
		else:
			found = False
			for d in polo_data:
				if d['orderNumber'] == self.id:
					found = True
					self.amount = float(d['amount'])
					self.update()
			
			if not found:
				self.drop()
				self.table_name = Order.ORDER_FILLED
				self.date_filled = time()
				self.save()

	##returns true if order is still active, else return false
	def is_active(self):
		if self.table_name == Order.ORDER_ACTIVE:
			return True
		else:
			return False

	##inserts trade into db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "INSERT INTO {tn} ({nf_id}, {nf_curr_pair}, {nf_date_placed}, {nf_date_filled}, {nf_amount}, {nf_rate}, {nf_type}) VALUES\
					({v_id}, '{v_curr_pair}', {v_date_placed}, {v_date_filled}, {v_amount}, {v_rate}, '{v_type}')"\
				.format(tn = self.table_name, nf_id = Order.ID, nf_curr_pair = Order.CURR_PAIR, nf_date_placed = Order.DATE_PLACED, nf_date_filled = Order.DATE_FILLED, nf_amount = Order.AMOUNT, nf_rate = Order.RATE, nf_type = Order.TYPE, v_id = self.id, v_curr_pair = self.curr_pair, v_date_placed = self.date_placed, v_date_filled = self.date_filled, v_amount = self.amount, v_rate = self.rate, v_type = self.type)
			cursor.execute(exec_string)

		except sqlite3.IntegrityError:
			print('ERROR: Something went wrong inserting order into {tn}'.format(tn = self.table_name))
		dbm.save_and_close()

	##drop order from the table that it is currently in
	def drop(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "DELETE FROM {tn}\
					WHERE {nf_id} = {v_id}"\
				.format(tn = self.table_name, nf_id = Order.ID, v_id = self.id)
			cursor.execute(exec_string)

		except sqlite3.IntegrityError:
			print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))
		dbm.save_and_close()

	##moves current order to new tn, updated amount_filled 
	def move(self, tn, amount_filled = 0):
		
		##drop from active orders
		self.drop()

		amount_left = self.amount

		##if any of the order was filled before being cancelled, create order
		if amount_filled > 0:
			self.table_name = Order.ORDER_FILLED 
			self.amount = amount_filled
			self.date_filled = time()
			self.save()

		if tn == self.ORDER_CANCELLED:
			self.table_name = tn 
			self.amount = amount_left
			self.date_filled = time()
			self.save()



	##updates an already existing trade
	def update(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "UPDATE {tn} SET {nf_curr_pair} = '{v_curr_pair}', {nf_date_placed} = {v_date_placed}, {nf_date_filled} = {v_date_filled}, {nf_amount} = {v_amount}, {nf_rate} = {v_rate}, {nf_type} = '{v_type}'\
					WHERE {nf_id} = {v_id}"\
				.format(tn = self.table_name, nf_id = Order.ID, nf_curr_pair = Order.CURR_PAIR, nf_date_placed = Order.DATE_PLACED, nf_date_filled = Order.DATE_FILLED, nf_amount = Order.AMOUNT, nf_rate = Order.RATE, nf_type = Order.TYPE, v_id = self.id, v_curr_pair = self.curr_pair, v_date_placed = self.date_placed, v_date_filled = self.date_filled, v_amount = self.amount, v_rate = self.rate, v_type = self.type)
			cursor.execute(exec_string)

		except sqlite3.IntegrityError:
			print('ERROR: Something went wrong inserting order into {tn}'.format(tn = self.table_name))
		dbm.save_and_close()
