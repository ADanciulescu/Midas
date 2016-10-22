##helper calculates rate of change of graphs

from point import Point

class ROCCalculator:
	def __init__(self, dbm, output_table_name, points):
		self.points = points
		self.output_table_name = output_table_name
		self.dbm = dbm
	
	##returns array of pts corresponding to moving average of points 
	def simple(self):
		
		##will eventually be returned
		pt_array = []

		for point_index, c in enumerate(self.points):
			## can't create ROC for i = 0
			roc = 0
			if point_index == 0:
				roc = 0
			elif point_index > 0:
				roc = self.points[point_index].value - self.points[point_index-1].value
			date = self.points[point_index].date
			pt = Point(self.dbm, self.output_table_name, date, roc)
			pt_array.append(pt)
		return pt_array
