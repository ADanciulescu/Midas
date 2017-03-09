## a table containing date , # of hits for each day of google trends 
## columns: date, hits
from db_manager import DBManager
from trend import Trend
from point_table import PointTable
from point import Point

class TrendTable:
	
	TEMP = "TEMP"
	
	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates trends table in db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_date} {ft_i} PRIMARY KEY {nn}, {nf_hits} {ft_i} {nn})'\
				.format(tn = self.table_name, nf_date = Trend.DATE, nf_hits = Trend.HITS, ft_i = DBManager.INTEGER, ft_t = DBManager.TEXT, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		dbm.save_and_close()
	
	## returns cursor to points between the 2 dates
	@staticmethod
	def get_section(table_name, date_start, date_end):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}' WHERE date > {ds} AND date < {de}".format(tn = table_name, ds = date_start, de = date_end))
		return cursor
	
	##returns trend objects for the given table_name
	@staticmethod
	def get_trend_array(table_name):
		##returns a cursor pointing to all candles linked to the table_name
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		trends = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Trend.from_tuple(table_name, row) 
			trends.append(t)
			row = cursor.fetchone()
		dbm.save_and_close()
		return trends

	##passed in a table_name and date
	##returns hits of the most recent trend before the given date
	@staticmethod
	def get_most_recent_hits(table_name, date):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		query = "SELECT hits FROM '{tn}' WHERE date < {d} ORDER BY date DESC".format(tn = table_name, d = date)
		cursor.execute(query)
		dbm.save_and_close()
		return cursor.fetchone()[0]

	
	##create point table using date and hits from trend_table_name, return its name
	@staticmethod
	def to_point_table(trend_table_name):
		pt_name = TrendTable.TEMP + "_" + trend_table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()
		trends = TrendTable.get_trend_array(trend_table_name)
		for t in trends:
			p = Point(pt_name, t.date, t.hits)
			p.save()
		return pt_name
