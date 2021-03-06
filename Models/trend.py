## model for google trend
## attributes: id , date, hits

import sqlite3
from db_manager import DBManager

class Trend:
	
	DATE = "date"
	HITS = "hits"

	def __init__(self, table_name, date, hits):
		self.table_name = table_name
		self.date = date
		self.hits = hits 

	##uses cursor tuple to create a Trend object and return it
	@staticmethod
	def from_tuple(table_name, tup):
		return Trend(table_name, tup[0], tup[1])
	
	def pprint(self):
		print()
		print(("table_name: ", self.table_name))
		print(("date: ", self.date))
		print(("hits: ", self.hits))
		print()
	
	##inserts trend into db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = "INSERT INTO {tn} ({nf_date}, {nf_hits}) VALUES\
				(\"{v_date}\", {v_hits})"\
			.format(tn = self.table_name, nf_date = self.DATE, nf_hits = self.HITS, v_date = self.date, v_hits = self.hits)
			
		try:
			cursor.execute(exec_string)
		except:
			print("Unable to insert trend into database, most likely a duplicate")
			
		dbm.save_and_close()
