## create a new trend table by creating a trend point for every candle
## trend point has the same date as the corresponding candle, and the # of hits = # of hits in the trendtable at most recent previous date

from candle_table import CandleTable
from trend_table import TrendTable
from trend import Trend
from db_manager import DBManager

class TrendCutter:

	def __init__(self, candle_table_name, trend_table_name):
		self.candle_table_name = candle_table_name
		self.trend_table_name = trend_table_name

	## calculates name of resulting trend table from dates and original trend table name
	def get_trend_table_name(self):
		return self.trend_table_name + '_' + str(self.first_date) + '_' + str(self.last_date)

		
	## creates a new table with a section from trend table	
	def create_cut_table(self):
		self.first_date = CandleTable.get_first_date(self.candle_table_name)
		self.last_date = CandleTable.get_last_date(self.candle_table_name)
		self.cut_trend_table_name = self.get_trend_table_name()

		if DBManager.exists_table(self.cut_trend_table_name):
			DBManager.drop_table(self.cut_trend_table_name)

		tt = TrendTable(self.cut_trend_table_name)
		tt.save()
	

		candles = CandleTable.get_candle_array(self.candle_table_name)

		for c in candles:
			date = c.date
			hits = TrendTable.get_most_recent_hits(self.trend_table_name, date)
			trend = Trend(dbm, self.cut_trend_table_name, date, hits)
			trend.save()
			
		##cursor = TrendTable.get_section(self.trend_table_name, self.first_date, self.last_date)
		##trend_tuples = cursor.fetchall()
		##for t in trend_tuples:
			##date = t[0]
			##hits = t[1]
			##trend = Trend(dbm, self.cut_trend_table_name, date, hits)
			##trend.save()
		##dbm.save_and_close()

		return tt

