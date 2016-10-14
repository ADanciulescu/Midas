## Model for data point consisting of pair of (date,value)
## attributes: id, date, value 

import sqlite3
from db_manager import DBManager
from point_table import PointTable

class Point:

	def __init__(self, db_manager, table_name, date, value):
		self.table_name = table_name
		self.db_manager = db_manager
		self.date = date
		self.value = value

	##uses cursor tuple to create a Point object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		dbm = DBManager()
		return Point(dbm, table_name, tup[1], tup[2])
	
	def pprint(self):
		print ""
		print "table_name: ", self.table_name
		print "date: ", self.date
		print "value: ", self.value
		print ""
	
	##inserts point into db
	def save(self):
		cursor = self.db_manager.get_cursor()
		try:
			cursor.execute("INSERT INTO {tn} ({nf_date}, {nf_value}) VALUES\
					({v_date}, {v_value})"\
				.format(tn = self.table_name, nf_date = PointTable.DATE, nf_value = PointTable.VALUE, v_date = self.date, v_value = self.value))
			
		except sqlite3.IntegrityError:
			    print('ERROR: Something went wrong inserting point into {tn}'.format(tn = table_name))
	
	##returns point objects for the given table_name
	@staticmethod
	def get_point_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = PointTable.get_point_cursor(table_name)
		points = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Point.from_tuple(table_name, row) 
			points.append(t)
			row = cursor.fetchone()
		return points
