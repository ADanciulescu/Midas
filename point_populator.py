## populates point tables with data

from moving_average import MovingAverage
from candle import Candle
from point import Point
from point_table import PointTable
from db_manager import DBManager

class PointPopulator():

	def __init__(self, table_name):
		self.table_name = table_name
	
	def create_moving_avg_simple(self):
		pt_name = self.table_name + "_AVG_SIMPLE"
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()



		candles = Candle.get_candle_array(self.table_name)
		dbm = DBManager()
		for i, c in enumerate(candles):
			mv = MovingAverage(candles, i)
			mvs = mv.simple()
			date = c.date
			p = Point(dbm, pt_name, date, mvs)
			p.save()
		dbm.save_and_close()

			




