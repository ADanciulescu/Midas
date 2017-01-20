## populates point tables with data

from moving_average import MovingAverage
from candle import Candle
from candle_table import CandleTable
from point import Point
from point_table import PointTable
from db_manager import DBManager
from roc_calculator import ROCCalculator
from trend_table import TrendTable

class PointPopulator():

	SIMPLE_AVG = "___SIMPLE_AVG"
	EXP_AVG = "___EXP_AVG"
	SIMPLE_ROC = "___SIMPLE_ROC"

	##possible values for type of input data
	CANDLE = "CANDLE"
	POINT = "POINT"
	TREND = "TREND"

	def __init__(self, table_name):
		self.table_name = table_name
		self.setup()

	## prepare to calculate point table
	def setup(self):
		if self.POINT in self.table_name:
			self.input_point_table_name = self.table_name
		elif self.TREND in self.table_name:
			self.input_point_table_name = TrendTable.to_point_table(self.table_name)
		else:
			self.input_point_table_name = CandleTable.to_point_table(self.table_name)

		self.output_table_name = self.table_name.replace(self.CANDLE, self.POINT)



	##passed in an array of pts, save each point
	def save_pts(self, dbm, pt_array):
		for p in pt_array:
			p.save()
		dbm.save_and_close()

	
	##calculates and inserts simple moving average points in sql table
	def create_moving_avg_simple(self, num_history_pts):
		self.output_table_name = self.output_table_name.replace("TREND", "POINT")
		self.output_table_name = self.output_table_name.replace("CANDLE", "POINT")
		print self.output_table_name
		self.output_table_name = self.output_table_name + self.SIMPLE_AVG + "_" + str(num_history_pts)
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(self.output_table_name):
			DBManager.drop_table(self.output_table_name)
		
		pt = PointTable(self.output_table_name)
		pt.save()
		
		points = PointTable.get_point_array(self.input_point_table_name)
		dbm = DBManager()
		mv = MovingAverage(dbm, self.output_table_name, points)
		pt_array = mv.simple(num_history_pts)
		self.save_pts(dbm, pt_array)
		
		## possible delete the temporary point table created from candle
		if CandleTable.TEMP in self.input_point_table_name:
			DBManager.drop_table(self.input_point_table_name)
		return self.output_table_name


	##calculates and inserts exponential moving average points in sql table
	def create_moving_avg_exp(self):
		self.output_table_name += self.EXP_AVG
		
		pt_name = self.table_name
		
		if DBManager.exists_table(self.output_table_name):
			DBManager.drop_table(self.output_table_name)
		
		pt = PointTable(self.output_table_name)
		pt.save()

		points = PointTable.get_point_array(self.input_point_table_name)
		dbm = DBManager()
		mv = MovingAverage(dbm, self.output_table_name, points)
		pt_array = mv.exponential()
		self.save_pts(dbm, pt_array)
		
		## possible delete the temporary point table created from candle
		if CandleTable.TEMP in self.input_point_table_name:
			DBManager.drop_table(self.input_point_table_name)
		
		return self.output_table_name



	##calculates and inserts simple roc points in sql table
	def create_roc(self):
		self.output_table_name += self.SIMPLE_ROC
		pt_name = self.table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(self.output_table_name):
			DBManager.drop_table(self.output_table_name)
		
		pt = PointTable(self.output_table_name)
		pt.save()

		points = PointTable.get_point_array(self.input_point_table_name)
		dbm = DBManager()
		r = ROCCalculator(dbm, self.output_table_name, points)
		pt_array = r.simple()
		self.save_pts(dbm, pt_array)
		
		## possible delete the temporary point table created from candle
		if CandleTable.TEMP in self.input_point_table_name:
			DBManager.drop_table(self.input_point_table_name)
		
		return self.output_table_name