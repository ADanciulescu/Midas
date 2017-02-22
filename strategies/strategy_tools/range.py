##used for short term strategy
##consists of 2 points where market movement is monotonic(based on candle close) between the 2 points

import math

class Range:

	def __init__(self, pt1, pt2, value):
		self.pt1 = pt1
		self.pt2 = pt2
		self.value = value
		self.calc_type()

	def calc_type(self):
		if self.pt1 is None or self.pt2 is None:
			self.type = "NONE"
		elif self.pt1.value <= self.pt2.value:
			self.type = "INC"
		elif self.pt1.value >= self.pt2.value:
			self.type = "DESC"

	def get_value_dif(self):
		return self.pt2.value - self.pt1.value

	def get_len(self):
		return (abs(self.pt2.date - self.pt1.date))/300.0

	def pprint(self):
		print "Len:", self.get_len(), "[", self.pt1.value, "------", self.pt2.value, "]", "Value: ", self.value, self.type

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
		return new_r

	@staticmethod
	##take a range and split it into to around the pt passed in
	def split(old_range, pt):
		if old_range.type == "INC":
			range1 = Range(old_range.pt1, pt, old_range.value)
			range2 = Range(pt, old_range.pt2, old_range.value)
		else:
			range1 = Range(old_range.pt2, pt, old_range.value)
			range2 = Range(pt, old_range.pt1, old_range.value)
		return (range1, range2)

	def get_size(self):
		return abs(self.pt1.value - self.pt2.value)
