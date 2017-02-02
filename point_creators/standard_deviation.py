##used to calculate standard deviation

import math

class StandardDeviation():

	##passed in a pt array and returns the simple standard deviation
	@staticmethod
	def simple(pt_array):
		num_points = len(pt_array)

		##calculate avg
		sum = 0
		for pt in pt_array:
			sum += pt.value
		avg = sum/float(num_points)
		
		##calculate sum of squares
		sos = 0
		for pt in pt_array:
			sos += (pt.value-avg)*(pt.value-avg)
		sos /= float(num_points-1)

		return math.sqrt(sos)

