## Model for data point consisting of pair of (date,value)
## attributes: id, date, value 

import sqlite3
from db_manager import DBManager

class Point:
	
	ID = "id"
	DATE = "date"
	VALUE = "value"

	def __init__(self, table_name, date, value):
		self.table_name = table_name
		self.date = date
		self.value = value

	##uses cursor tuple to create a Point object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Point(table_name, tup[1], tup[2])
	
	def pprint(self):
		print()
		print(("table_name: ", self.table_name))
		print(("date: ", self.date))
		print(("value: ", self.value))
		print()
	
	##inserts point into db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_value}) VALUES\
					({v_date}, {v_value})"\
				.format(tn = self.table_name, nf_date = Point.DATE, nf_value = Point.VALUE, v_date = self.date, v_value = self.value))
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting point into {tn}'.format(tn = table_name))
	
