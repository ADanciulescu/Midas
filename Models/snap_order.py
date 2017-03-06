## Model for snap order 
## attributes: date, value 

import sqlite3
from db_manager import DBManager

class SnapOrder:
	
	DATE = "date"
	AMOUNT = "amount"
	RATE = "rate"
	TYPE = "type"

	def __init__(self, table_name, date, amount, rate, type):
		self.table_name = table_name
		self.date = date
		self.amount = amount
		self.rate = rate
		self.type = type

	##uses cursor tuple to create a SnapOrder object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return SnapOrder(table_name, tup[0], tup[1], tup[2], tup[3])
	
	
	##inserts snaporder into db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			query = "INSERT INTO {tn} ({nf_date}, {nf_amount}, {nf_rate}, {nf_type}) VALUES\
					({v_date}, {v_amount}, {v_rate}, '{v_type}')"\
				.format(tn = self.table_name, nf_date = SnapOrder.DATE, nf_amount = SnapOrder.AMOUNT, nf_rate = SnapOrder.RATE, nf_type = SnapOrder.TYPE, v_date = self.date, v_amount = self.amount, v_rate = self.rate, v_type = self.type)
			cursor.execute(query)
			dbm.save_and_close()

		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting snap order into {tn}'.format(tn = self.table_name))
