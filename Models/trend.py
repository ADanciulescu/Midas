## model for google trend
## attributes: id , date, hits

import sqlite3
from db_manager import DBManager
from trend_table import TrendTable

class Trend:

	def __init__(self, db_manager, table_name, date, hits):
		self.table_name = table_name
		self.db_manager = db_manager
		self.date = date
		self.hits = hits 

	##uses cursor tuple to create a Trend object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		dbm = DBManager()
		return Trend(dbm, table_name, tup[0], tup[1])
	
	def pprint(self):
		print ""
		print "table_name: ", self.table_name
		print "date: ", self.date
		print "hits: ", self.hits
		print ""
	
	##inserts trend into db
	def save(self):
		cursor = self.db_manager.get_cursor()
		exec_string = "INSERT INTO {tn} ({nf_date}, {nf_hits}) VALUES\
				(\"{v_date}\", {v_hits})"\
			.format(tn = self.table_name, nf_date = TrendTable.DATE, nf_hits = TrendTable.HITS, v_date = self.date, v_hits = self.hits)
		
		try:
			cursor.execute(exec_string)
		except:
			print "Unable to insert trend into database, most likely a duplicate"
			
	
	##returns trend objects for the given table_name
	@staticmethod
	def get_trend_array(table_name):
		##returns a cursor pointing to all candles linked to the table_name
		cursor = TrendTable.get_trend_cursor(table_name)
		trends = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Trend.from_tuple(table_name, row) 
			trends.append(t)
			row = cursor.fetchone()
		return trends
