## Model for trade performed by strategy 
## attributes:  date, amount, price, type

import sqlite3
from db_manager import DBManager

class Trade:
	
	DATE = "date"
	AMOUNT = "amount"
	PRICE = "price"
	TYPE = "type"
	BUY_TYPE = "BUY_TYPE"
	SELL_TYPE = "SELL_TYPE"
	NONE_TYPE = "NONE_TYPE"
	FAIL_SELL_TYPE = "FAIL_SELL_TYPE"
	FAIL_BUY_TYPE = "FAIL_BUY_TYPE"

	def __init__(self, table_name, date, amount, price, type):
		self.table_name = table_name
		self.date = date
		self.amount = amount
		self.price = price
		self.type = type

	##uses cursor tuple to create a Point object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Trade(table_name, tup[0], tup[1], tup[2], tup[3])
	
	def pprint(self):
		if self.type == self.BUY_TYPE:
			print(("Bought: ", self.amount, " at: ", self.price))
		elif self.type == self.SELL_TYPE:
			print(("Sold: ", self.amount, " at: ", self.price))
		elif self.type == self.FAIL_SELL_TYPE:
			print(("Fail to sell: ", self.amount, " at: ", self.price))
		elif self.type == self.FAIL_BUY_TYPE:
			print(("Fail to buy: ", self.amount, " at: ", self.price))



	##inserts trade into db
	def save(self, to_commit = False):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "INSERT INTO {tn} ({nf_date}, {nf_amount}, {nf_price}, {nf_type}) VALUES\
					({v_date}, {v_amount}, {v_price}, '{v_type}')"\
				.format(tn = self.table_name, nf_date = Trade.DATE, nf_amount = Trade.AMOUNT, nf_price = Trade.PRICE, nf_type = Trade.TYPE, v_date = self.date, v_amount = self.amount, v_price = self.price, v_type = self.type)
			cursor.execute(exec_string)
			
			##for speed purposes only commit when changing one at a time
			if to_commit:
				dbm.conn.commit()

		except sqlite3.IntegrityError:
			pass 
			##print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))
		dbm.save_and_close()

	##updates an already existing trade
	def update(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "UPDATE {tn} SET {nf_amount} = {v_amount}, {nf_price} = {v_price}, {nf_type} = '{v_type}'\
					WHERE {nf_date} = {v_date}"\
				.format(tn = self.table_name, nf_date = Trade.DATE, nf_amount = Trade.AMOUNT, nf_price = Trade.PRICE, nf_type = Trade.TYPE, v_date = self.date, v_amount = self.amount, v_price = self.price, v_type = self.type)
			cursor.execute(exec_string)
			
			##for speed purposes only commit when changing one at a time
			dbm.conn.commit()
		except sqlite3.IntegrityError:
			print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))
		dbm.save_and_close()

