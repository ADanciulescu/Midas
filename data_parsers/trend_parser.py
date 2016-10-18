##parses trends and puts it in database

from db_manager import DBManager
from trend import Trend
from tools import date_to_timestamp

class TrendParser():

	def __init__(self, table_name, data):
		self.table_name = table_name
		self.data = data
	
	##inserts all of the trends into the db
	def insert(self):
		rows = self.data["table"]["rows"]
		dbm = DBManager()
		for r in rows:
			try:
				date_string = r["c"][0]["v"]
				print date_string
				date = date_to_timestamp(date_string)
				hits = r["c"][1]["f"]
				t = Trend(dbm, self.table_name, date, hits)
				t.save()
			except:
				print "rached the end"
		dbm.save_and_close()

