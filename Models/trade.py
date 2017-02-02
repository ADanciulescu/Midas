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

	def __init__(self, db_manager, table_name, date, amount, price, type):
		self.table_name = table_name
		self.db_manager = db_manager
		self.date = date
		self.amount = amount
		self.price = price
		self.type = type

	##uses cursor tuple to create a Point object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		dbm = DBManager()
		return Trade(dbm, table_name, tup[0], tup[1], tup[2], tup[3])
	
	def pprint(self):
		if self.type == self.BUY_TYPE:
			print "Bought: " + str(self.amount) + " at: " + str(self.price)
		elif self.type == self.SELL_TYPE:
			print "Sold: " + str(self.amount) + " at: " + str(self.price)
		elif self.type == self.FAIL_SELL_TYPE:
			print "Fail to sell: " + str(self.amount) + " at: " + str(self.price)



	##inserts trade into db
	def save(self, to_commit = False):
		cursor = self.db_manager.get_cursor()
		try:
			exec_string = "INSERT INTO {tn} ({nf_date}, {nf_amount}, {nf_price}, {nf_type}) VALUES\
					({v_date}, {v_amount}, {v_price}, '{v_type}')"\
				.format(tn = self.table_name, nf_date = Trade.DATE, nf_amount = Trade.AMOUNT, nf_price = Trade.PRICE, nf_type = Trade.TYPE, v_date = self.date, v_amount = self.amount, v_price = self.price, v_type = self.type)
			cursor.execute(exec_string)
			
			##for speed purposes only commit when changing one at a time
			if to_commit:
				self.db_manager.conn.commit()

		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))

	##updates an already existing trade
	def update(self):
		cursor = self.db_manager.get_cursor()
		try:
			exec_string = "UPDATE {tn} SET {nf_amount} = {v_amount}, {nf_price} = {v_price}, {nf_type} = '{v_type}'\
					WHERE {nf_date} = {v_date}"\
				.format(tn = self.table_name, nf_date = Trade.DATE, nf_amount = Trade.AMOUNT, nf_price = Trade.PRICE, nf_type = Trade.TYPE, v_date = self.date, v_amount = self.amount, v_price = self.price, v_type = self.type)
			cursor.execute(exec_string)
			
			##for speed purposes only commit when changing one at a time
			self.db_manager.conn.commit()

		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))

