## fetches trends from google api

from pytrends.request import TrendReq
from trend_parser import TrendParser
from db_manager import DBManager
from trend_table import TrendTable

class TrendFetcher:
	## num_months less than 4 will give daily level data
	## date format is "01/2015" etc
	def __init__(self, table_name, keyword, date, num_months):
		self.username = "andr1357@gmail.com"
		self.password = "mifune1423"
		
		self.table_name = table_name
		self.keyword = keyword
		self.date = date
		self.num_months = num_months
		self.pytrend = TrendReq(self.username, self.password, custom_useragent='Midas Trends')
		self.payload = {'q': keyword, 'date': date + " " + str(num_months) + "m"}
	
		##creates table if it doesnt already exist
		if not DBManager.exists_table(table_name):
			tt = TrendTable(table_name)
			tt.save()
	
	def fetch(self):
		data = self.pytrend.trend(self.payload)
		tp = TrendParser(self.table_name, data)
		tp.insert()




