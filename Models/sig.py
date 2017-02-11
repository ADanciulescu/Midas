## produced by signaler 
## a signal notifies that it is time to buy/sell

import sqlite3
from db_manager import DBManager
from tools import timestamp_to_date

class Sig:
	
	##possible types
	BUY = "BUY"
	SELL = "SELL"

	DATE = "date"
	SYM = "sym"
	AMOUNT = "amount"
	PRICE = "price"
	TYPE = "type"

	def __init__(self, table_name, date, sym, amount, price, type):
		self.table_name = table_name
		self.date = date ## candle date that set off the signal
		self.sym = sym
		self.amount = amount
		self.price = price
		self.type = type

	##uses cursor tuple to create a Sig object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Sig(table_name, tup[0], tup[1], tup[2], tup[3], tup[4])
	
	def pprint(self):
		print self.summary()  
	
	def summary(self):
		return self.sym + " " + self.type + " " + timestamp_to_date(self.date) + " " + str(self.amount) + " at $" + str(self.price)  

	##inserts point into db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "INSERT INTO {tn} ({nf_date}, {nf_sym}, {nf_amount}, {nf_price}, {nf_type}) VALUES\
					({v_date}, \"{v_sym}\", {v_amount}, {v_price}, \"{v_type}\")"\
				.format(tn = self.table_name, nf_date = Sig.DATE, nf_sym = self.SYM, nf_amount = Sig.AMOUNT, nf_price = Sig.PRICE,
					nf_type = Sig.TYPE, v_date = self.date, v_sym = self.sym, v_amount = self.amount, v_price = self.price, v_type = self.type)
			cursor.execute(exec_string)
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting signal into {tn}'.format(tn = table_name))

