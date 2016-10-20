## populates point tables with data

from moving_average import MovingAverage
from candle import Candle
from point import Point
from point_table import PointTable
from db_manager import DBManager
from roc_calculator import ROCCalculator

class PointPopulator():

	SIMPLE_AVG = "___SIMPLE_AVG"
	EXP_AVG = "___EXP_AVG"
	SIMPLE_ROC = "___SIMPLE_ROC"

	def __init__(self, table_name):
		self.table_name = table_name
		self.candle_table_name = table_name.split("___")[0]

	##passed in an array of pts, save each point
	def save_pts(self, dbm, pt_array):
		for p in pt_array:
			p.save()
		dbm.save_and_close()
	
	##calculates and inserts simple moving average points in sql table
	def create_moving_avg_simple(self, num_history_pts):
		pt_name = self.table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()

		candles = Candle.get_candle_array(self.candle_table_name)
		dbm = DBManager()
		mv = MovingAverage(dbm, pt_name, candles)
		pt_array = mv.simple(num_history_pts)
		self.save_pts(dbm, pt_array)


	##calculates and inserts exponential moving average points in sql table
	def create_moving_avg_exp(self):

		pt_name = self.table_name
		
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()

		candles = Candle.get_candle_array(self.candle_table_name)
		dbm = DBManager()
		mv = MovingAverage(dbm, pt_name, candles)
		pt_array = mv.exponential()
		self.save_pts(dbm, pt_array)


	##calculates and inserts simple roc points in sql table
	def create_roc(self):
		pt_name = self.table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()

		candles = Candle.get_candle_array(self.candle_table_name)
		dbm = DBManager()
		r = ROCCalculator(dbm, pt_name, candles)
		pt_array = r.simple()
		self.save_pts(dbm, pt_array)
