##helper called by strategies that computes various types of moving average

from candle import Candle
from point_table import PointTable

class MovingAverage:
	def __init__(self, table_name, candles, time):
		self.candles = candles
		self.time = time
		self.table_name = table_name
	
	##number of points considered in moving average
	##TODO: possibly change later to adjust number of points used based on time between points(effectively holding time for average constant and not the # of points)
	POINTS_SIMPLE = 10

	##returns simple moving average of the graph(specified by candles)at the given time 
	def simple(self):

		total = 0
		avg = 0

		##special case with less points
		if self.time < (self.POINTS_SIMPLE):
			for i in range(0, self.time + 1):
				total += self.candles[i].mid
			avg = total/(self.time + 1)
		else:
			for i in range(self.time - self.POINTS_SIMPLE, self.time):
				total += self.candles[i].mid
			avg = total/(self.POINTS_SIMPLE)
		return avg

	ALPHA = 0.5
	## returns exponentially smoothed average
	## equal to alpha*current_close + (1-alpha)*last smoothed average
	def exponential(self):
		print self.time
		if self.time == 0:
			return self.candles[0].close
		else:
			cur_close = self.candles[self.time].close
			past_avg = PointTable.lookup(self.table_name, self.time)[0]
			return (self.ALPHA * cur_close) + (1 - self.ALPHA)*past_avg







