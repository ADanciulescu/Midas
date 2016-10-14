##helper called by strategies that computes various types of moving average

from candle import Candle

class MovingAverage:
	def __init__(self, candles, time):
		self.candles = candles
		self.time = time
	
	##number of points considered in moving average
	##TODO: possibly change later to adjust number of points used based on time between points(effectively holding time for average constant and not the # of points)
	POINTS_SIMPLE = 10

	##returns simple moving average of the graph(specified by candles)at the given time 
	def simple(self):

		total = 0
		avg = 0

		##special case with less points
		if self.time < (self.POINTS_SIMPLE - 1 ):
			for i in range(0, self.time + 1):
				total += self.candles[i].mid
			avg = total/(self.time + 1)
		else:
			for i in range(self.time - self.POINTS_SIMPLE, self.time +1):
				total += self.candles[i].mid
			avg = total/(self.POINTS_SIMPLE)
		return avg





