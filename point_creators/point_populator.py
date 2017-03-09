## populates point tables with data

from moving_average import MovingAverage
from candle import Candle
from candle_table import CandleTable
from point import Point
from point_table import PointTable
from db_manager import DBManager
from roc_calculator import ROCCalculator
from trend_table import TrendTable
from standard_deviation import StandardDeviation

class PointPopulator():

	SIMPLE_AVG = "___SIMPLE_AVG"
	EXP_AVG = "___EXP_AVG"
	SIMPLE_ROC = "___SIMPLE_ROC"
	VOLUME = "___VOLUME"
	STDDEV = "___STDDEV"
	OSCIL = "___OSCIL"

	##possible values for type of input data
	CANDLE = "CANDLE"
	POINT = "POINT"
	TREND = "TREND"

	def __init__(self, table_name, to_save = False):
		self.table_name = table_name
		self.to_save = to_save

		self.setup()

	## prepare to calculate point table
	def setup(self):
		if self.POINT in self.table_name:
			self.input_points = PointTable.to_point_array(self.table_name)
		elif self.TREND in self.table_name:
			self.input_points = TrendTable.to_point_array(self.table_name)
		else:
			self.input_points = CandleTable.to_point_array(self.table_name, "close")

		self.output_table_name = self.table_name.replace(self.CANDLE, self.POINT)



	##passed in an array of pts, save each point
	def save_pts(self, pt_array):
		for p in pt_array:
			p.save()



	##calculate standard deviation table for num_history_points
	def create_stddev(self, num_history_pts):
		self.output_table_name = self.output_table_name.replace("TREND", "POINT")
		self.output_table_name = self.output_table_name.replace("CANDLE", "POINT")
		self.output_table_name = self.output_table_name + self.STDDEV + "_" + str(num_history_pts)

		if self.to_save:
			##if already exists, drop it first and then recreate
			if DBManager.exists_table(self.output_table_name):
				DBManager.drop_table(self.output_table_name)
			
			pt = PointTable(self.output_table_name)
			pt.save()

		orig_pt_array = self.input_points
		stddev_pt_array = []

		for i, pt in enumerate(orig_pt_array):
			if i < num_history_pts: ##don't calculate stddev for first points since there is not enough history available
				pass
			else:
				date = pt.date
				stddev = StandardDeviation.simple(orig_pt_array[i-num_history_pts + 1: i+ 1])
				stddev_pt = Point(self.output_table_name, date, stddev)
				stddev_pt_array.append(stddev_pt)
		
		if self.to_save:
			self.save_pts(stddev_pt_array)

		##if CandleTable.TEMP in self.input_point_table_name:
		##	DBManager.drop_table(self.input_point_table_name)
		
		return stddev_pt_array
	
	## calculates and returns an array of points representing oscillator
	## oscillator point is the difference between candle_close now - candle_close period ago 
	def create_oscil(self, period):
		self.output_table_name = self.output_table_name.replace("TREND", "POINT")
		self.output_table_name = self.output_table_name.replace("CANDLE", "POINT")
		self.output_table_name = self.output_table_name + self.OSCIL + "_" + str(period)
		
		if self.to_save:
			##if already exists, drop it first and then recreate
			if DBManager.exists_table(self.output_table_name):
				DBManager.drop_table(self.output_table_name)
			
			pt = PointTable(self.output_table_name)
			pt.save()
		
		oscil_pt_array = []

		for i, pt in enumerate(self.input_points):
			if i < (period-1): ##don't calculate stddev for first points since there is not enough history available
				pass
			else:
				date = pt.date
				oscil_value = pt.value - self.input_points[i-period].value
				oscil_pt = Point(self.output_table_name, date, oscil_value)
				oscil_pt_array.append(oscil_pt)
		
		
		if self.to_save:
			self.save_pts(oscil_pt_array)
		
		return oscil_pt_array
	
	
	##calculates and inserts simple moving average points in sql table
	def create_moving_avg_simple(self, num_history_pts):
		self.output_table_name = self.output_table_name.replace("TREND", "POINT")
		self.output_table_name = self.output_table_name.replace("CANDLE", "POINT")
		self.output_table_name = self.output_table_name + self.SIMPLE_AVG + "_" + str(num_history_pts)
		
		if self.to_save:
			##if already exists, drop it first and then recreate
			if DBManager.exists_table(self.output_table_name):
				DBManager.drop_table(self.output_table_name)
			
			pt = PointTable(self.output_table_name)
			pt.save()
		
		points = self.input_points 
		mv = MovingAverage(self.output_table_name, points)
		pt_array = mv.simple(num_history_pts)
		
		if self.to_save:
			self.save_pts(pt_array)
		
		## possible delete the temporary point table created from candle
		##if CandleTable.TEMP in self.input_point_table_name:
		##	DBManager.drop_table(self.input_point_table_name)
		
		return pt_array


	##calculates and inserts exponential moving average points in sql table
	def create_moving_avg_exp(self):
		self.output_table_name += self.EXP_AVG
		
		pt_name = self.table_name
		
		if DBManager.exists_table(self.output_table_name):
			DBManager.drop_table(self.output_table_name)
		
		pt = PointTable(self.output_table_name)
		pt.save()

		points = self.input_points 
		mv = MovingAverage(self.output_table_name, points)
		pt_array = mv.exponential()
		self.save_pts(pt_array)
		
		## possible delete the temporary point table created from candle
		##if CandleTable.TEMP in self.input_point_table_name:
		##	DBManager.drop_table(self.input_point_table_name)
		
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

		points = self.input_points 
		r = ROCCalculator(self.output_table_name, points)
		pt_array = r.simple()
		self.save_pts(pt_array)
		
		## possible delete the temporary point table created from candle
		##if CandleTable.TEMP in self.input_point_table_name:
		##	DBManager.drop_table(self.input_point_table_name)
		
		return self.output_table_name
