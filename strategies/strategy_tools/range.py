##used for short term strategy
##consists of 2 points where market movement is monotonic(based on candle close) between the 2 points

import math

class Range:

	def __init__(self, pt1, pt2):
		self.pt1 = pt1
		self.pt2 = pt2
		
	def calc_type(self):
		if self.pt1.value <= self.pt2.value:
			self.type = "INC"
		else:
			self.type = "DESC"
	
	def get_len(self):
		return (self.pt2.date - self.pt1.date)/300

	def pprint(self):
		print "Len:", self.get_len(), "[", self.pt1.value, "------", self.pt2.value, "]", self.type

	def is_between(self, val):
		if self.type == "INC":
			if self.pt1.value <= val <= self.pt2.value:
				return True
			else:
				return False
		else:
			if self.pt2.value <= val <= self.pt1.value:
				return True
			else:
				return False

	@staticmethod
	def merge(r1, r2):
		new_r = Range(r1.pt1, r2.pt2)
		new_r.calc_type()
		return new_r

	def get_size(self):
		return abs(self.pt1.value - self.pt2.value)
