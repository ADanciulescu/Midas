## Model for snapshot of order book at date for a certain currency
## attributes: date 

import sqlite3
from db_manager import DBManager
from snap_order_table import SnapOrderTable

class Snap:
	
	DATE = "date"

	def __init__(self, table_name, date):
		self.table_name = table_name
		self.date = date

		self.order_table_name = SnapOrderTable.create_name(table_name)

	##uses cursor tuple to create a Snap object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Snap(table_name, tup[0])
	
	
	##inserts snap into db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			query = "INSERT INTO {tn} VALUES\
					({v_date})"\
				.format(tn = self.table_name, nf_date = Snap.DATE, v_date = self.date)
			cursor.execute(query)
			dbm.save_and_close()
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting snap into {tn}'.format(tn = self.table_name))
	
