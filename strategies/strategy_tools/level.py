## used for short term strategy
## stores information about how many ranges cross the "level_val"

class Level:
	
	def __init__(self, val, ranges):
		self.val = val
		self.ranges = ranges
		self.total = 0
		self.num_ranges = 0
	
	##updates total and num_ranges
	def update_stats(self):
		self.num_ranges = len(self.ranges)
		self.total = 0
		for r in self.ranges:
			self.total += r.get_size()
	
	def pprint(self):
			print self.val, "Num Ranges:", self.num_ranges, "Total:", self.total, "Avg: ", self.total/self.num_ranges
