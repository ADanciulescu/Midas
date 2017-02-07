##helper called by strategies that computes various types of moving average

from point_table import PointTable
from point import Point

class MovingAverage:
	def __init__(self, output_table_name, points):
		self.points = points
		self.output_table_name = output_table_name
	
	##number of points considered in moving average
	##TODO: possibly change later to adjust number of points used based on time between points(effectively holding time for average constant and not the # of points)
	POINTS_SIMPLE = 10

	##returns array of pts corresponding to moving average of points 
	def simple_slow(self, num_history_pts):
		
		##will eventually be returned
		pt_array = []

		for point_index, c in enumerate(self.points):

			total = 0
			avg = 0

			##special case with less points
			if point_index < (num_history_pts):
				for i in range(0, point_index + 1):
					total += self.points[i].value
				avg = total/(point_index + 1)
			else:
				for i in range(point_index - num_history_pts + 1, point_index + 1):
					total += self.points[i].value
				avg = total/(num_history_pts)

			date = self.points[point_index].date

			pt = Point(self.output_table_name, date, avg)
			pt_array.append(pt)
		return pt_array
	
	##returns array of pts corresponding to moving average of points 
	def simple(self, num_history_pts):
		
		##will eventually be returned
		pt_array = []

		for point_index, c in enumerate(self.points):

			total = 0
			avg = 0

			##special case with less points
			if point_index < (num_history_pts):
				for i in range(0, point_index + 1):
					total += self.points[i].value
				avg = total/(point_index + 1)
			else:
				old_avg = pt_array[-1].value
				old_total = old_avg * num_history_pts 
				##substract the oldest point contained in old_avg
				new_total = old_total - self.points[point_index- num_history_pts].value
				##add newest point
				new_total += self.points[point_index].value
				new_avg = new_total/num_history_pts
				avg = new_avg
			
			date = self.points[point_index].date
			pt = Point(self.output_table_name, date, avg)
			pt_array.append(pt)
		return pt_array

	ALPHA = 0.5
	## returns pt array of exponentially smoothed average
	## equal to alpha*current_close + (1-alpha)*last smoothed average
	def exponential(self):
		pt_array = []
		for point_index, c in enumerate(self.points):
			avg = 0
			if point_index == 0:
				avg = self.points[0].value
			else:
				cur_close = self.points[point_index].value
				past_avg = pt_array[point_index - 1].value
				avg =  (self.ALPHA * cur_close) + (1 - self.ALPHA)*past_avg
			date = self.points[point_index].date
			pt = Point(self.output_table_name, date, avg)
			pt_array.append(pt)
		return pt_array







