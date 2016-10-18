## populates point tables with data

from moving_average import MovingAverage
from candle import Candle
from point import Point
from point_table import PointTable
from db_manager import DBManager

class PointPopulator():

	SIMPLE_AVG = "___SIMPLE_AVG"
	EXP_AVG = "___EXP_AVG"
	SIMPLE_ROC = "___SIMPLE_ROC"

	def __init__(self, table_name):
		self.table_name = table_name
		self.candle_table_name = table_name.split("___")[0]

	##based on table name it decides what type of points to populate with
	def populate(self):
			if self.SIMPLE_AVG in self.table_name:
				self.create_moving_avg_simple()
			elif self.EXP_AVG in self.table_name:
				self.create_moving_avg_exp()
			elif self.SIMPLE_ROC in self.table_name:
				self.create_roc()
	
	def create_moving_avg_simple(self):
		pt_name = self.table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()

		candles = Candle.get_candle_array(self.candle_table_name)
		dbm = DBManager()
		for i, c in enumerate(candles):
			mv = MovingAverage(self.table_name, candles, i)
			mvs = mv.simple()
			date = c.date
			p = Point(dbm, pt_name, date, mvs)
			p.save()
		dbm.save_and_close()


	def create_moving_avg_exp(self):

		pt_name = self.table_name
		
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()

		candles = Candle.get_candle_array(self.candle_table_name)
		dbm = DBManager()
		for i, c in enumerate(candles):
			print "wtf"
			mv = MovingAverage(self.table_name, candles, i)
			mvs = mv.exponential()
			date = c.date
			p = Point(dbm, pt_name, date, mvs)
			p.save()
			dbm.conn.commit()
		dbm.save_and_close()



	def create_roc(self):
		pt_name = self.table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()

		candles = Candle.get_candle_array(self.candle_table_name)
		dbm = DBManager()
		for i, c in enumerate(candles):
			## can't create ROC for i = 0
			if i > 0:

				roc_val = candles[i].mid - candles[i-1].mid
				date = c.date
				p = Point(dbm, pt_name, date, roc_val)
				p.save()
		dbm.save_and_close()

