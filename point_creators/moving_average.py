##helper called by strategies that computes various types of moving average

from candle import Candle
from point_table import PointTable
from point import Point

class MovingAverage:
	def __init__(self, dbm, pt_table_name, candles):
		self.candles = candles
		self.pt_table_name = pt_table_name
		self.dbm = dbm
	
	##number of points considered in moving average
	##TODO: possibly change later to adjust number of points used based on time between points(effectively holding time for average constant and not the # of points)
	POINTS_SIMPLE = 10

	##returns array of pts corresponding to moving average of candles 
	def simple(self, num_history_pts):
		
		##will eventually be returned
		pt_array = []

		for candle_index, c in enumerate(self.candles):

			total = 0
			avg = 0

			##special case with less points
			if candle_index < (num_history_pts):
				for i in range(0, candle_index + 1):
					total += self.candles[i].mid
				avg = total/(candle_index + 1)
			else:
				for i in range(candle_index - num_history_pts, candle_index):
					total += self.candles[i].mid
				avg = total/(num_history_pts)

			date = self.candles[candle_index].date

			pt = Point(self.dbm, self.pt_table_name, date, avg)
			pt_array.append(pt)
		return pt_array

	ALPHA = 0.5
	## returns pt array of exponentially smoothed average
	## equal to alpha*current_close + (1-alpha)*last smoothed average
	def exponential(self):
		pt_array = []
		for candle_index, c in enumerate(self.candles):
			avg = 0
			if candle_index == 0:
				avg = self.candles[0].close
			else:
				cur_close = self.candles[candle_index].close
				past_avg = pt_array[candle_index - 1].value
				avg =  (self.ALPHA * cur_close) + (1 - self.ALPHA)*past_avg
			date = self.candles[candle_index].date
			pt = Point(self.dbm, self.pt_table_name, date, avg)
			pt_array.append(pt)
		return pt_array







