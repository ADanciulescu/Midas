## used by short term strategy
## stores intervals that aggregate ranges travelled by price

from range import Range

class Area:

	def __init__(self, low_min, high_min):
		self.low_min = low_min
		self.high_min = high_min

	def is_between(self, val):
		if val >= self.low_min and val <= self.high_min:
			return True
		else:
			return False

	def calculate_limits(self, interval_array):
		self.mid = interval_array.find_percentile(self.low_min, self.high_min, 0.5)
		if interval_array.height_at(self.mid) < 1:
			self.low_limit = -1
			self.high_limit = -1
		else:
			self.low_limit = interval_array.find_percentile(self.low_min, self.high_min, 0.2)
			self.high_limit = interval_array.find_percentile(self.low_min, self.high_min, 0.8)
			
			if (self.high_limit-self.low_limit)*2/(self.high_limit+self.low_limit) < 0.003:
				self.low_limit = -10
				self.high_limit = -10

class IntervalArray:

	def __init__(self, interval_array):
		self.interval_array = interval_array
		self.cumulative_array = []
		self.local_mins = []
		self.local_maxes = []

	def add_ranges(self, ranges):
		for r in ranges:
			self.add_range(r)

	def height_at(self, val):
		for i in self.interval_array:
			if i.is_between(val):
				return i.value
	
	##updates interval arrange by adding the range given
	def add_range(self, r):
		self.add_key_pt(r.pt1)	
		self.add_key_pt(r.pt2)
		self.update_interval_values(r, 1)
	
	##updates interval arrange by deleting the range given
	def delete_range(self, r):
		self.update_interval_values(r, -1)
		self.delete_key_pt(r.pt1)
		self.delete_key_pt(r.pt2)
	
	def update_intervals(self):
		self.find_local_mins()
		self.calc_cumulative()
		##self.find_local_maxes()

	def calc_cumulative(self):
		self.cumulative_array = []
		for i, interval in enumerate(self.interval_array):
			if i == 0:
				new_interval = Range(interval.pt1, interval.pt2, interval.value* interval.get_value_dif())
			else:
				new_interval = Range(interval.pt1, interval.pt2, (interval.value*interval.get_value_dif()) + self.cumulative_array[-1].value)
			##new_interval.pprint()
			self.cumulative_array.append(new_interval)
	
	def area_between(self, begin, end):
		area_begin = 0
		area_end = 0
		for i, c in enumerate(self.cumulative_array):
			if c.is_between(begin):
				##if we are in the first interval
				if i == 0:
					area_begin = (begin-c.pt1.value)* self.interval_array[i].value
				else:
					area_begin = self.cumulative_array[i-1].value + (begin-c.pt1.value)* self.interval_array[i].value
				##print "area:begin"
				##print i
				##print area_begin
			if c.is_between(end):
				if i == 0:
					area_end = (end - c.pt1.value)*self.interval_array[i].value
				else:
					area_end = self.cumulative_array[i-1].value + (end - c.pt1.value)*self.interval_array[i].value
				##print "area:end"
				##print i
				##print area_end
		return area_end - area_begin

	def find_local_maxes(self):
		self.local_maxes = []
		i = 0
		while i < len(self.local_mins)-1:	
			local_max = self.find_percentile(self.local_mins[i], self.local_mins[i+1], 0.5)
			##g = raw_input("")
			##print local_max
			self.local_maxes.append(local_max)
			i += 1

	##finds closest max to the passed in value
	##returns low_limit and high_limit around the max to be used to make trade decisions
	def get_limits(self, val):
		##g = raw_input("")
		##dif_array = []
		##for m in self.local_maxes:
			##dif_array.append(abs(m-val))

		##min_diff = dif_array[0]
		##min_index = 0
		##for i, d in enumerate(dif_array):
			##if d< min_diff:
				##min_diff = d
				##min_index = i
		target_area = None
		for a in self.areas:
			if a.is_between(val):
				target_area = a

		if target_area is None:
			##print val 
			##self.pprint()
			return (-1, -1)
		else:
			target_area.calculate_limits(self)
			return (target_area.low_limit, target_area.high_limit)

		##low_limit = self.find_percentile(self.local_mins[min_index], self.local_mins[min_index+1], 0.2)
		##high_limit = self.find_percentile(self.local_mins[min_index], self.local_mins[min_index+1], 0.8)
		
		##if (high_limit-low_limit)*2/(high_limit+low_limit) > 0.004:
			##return(low_limit, high_limit)
		##else:
			##return (-1 , -1)

	
	##given 2 endpoints binary search for the value between endpoints corresponding to the percentile p
	## for example p = 0.5 will find the value such that the area between start and value is 50% of the area between start and end
	def find_percentile(self, start, end, p):
		target_area = self.area_between(start, end)*p
		return self.find_percentile_area(start, end, target_area)

	##uses area instead of percentile, helper for find_percentile
	def find_percentile_area(self, start, end, area):
		guess = (start+end)/2
		##print start, end, area
		##print "Guess:", guess
		guess_area = self.area_between(start, guess)
		##print "Guess Area:",  guess_area
		##g = raw_input("")
		if abs(area - guess_area) > 0.01:
				if guess_area > area :
					##print "too high"
					return self.find_percentile_area(start, guess, area)
				else:
					##print "too low"
					return self.find_percentile_area(guess, end, area-guess_area)
		else:
			return guess

	
	def find_local_mins(self):
		self.local_mins =[]
		##agg array groups adjacet intervals that have the same value
		agg_array = []
		for i,interval in enumerate(self.interval_array):
			if agg_array == []:
				agg_array.append([interval])
			else:
				if agg_array[-1][0].value == interval.value:
					agg_array[-1].append(interval)
				else:
					agg_array.append([interval])
		
		##first_local_min = (agg_array[0][-1].pt2.value + agg_array[0][0].pt1.value)/2
		first_local_min = agg_array[0][0].pt1.value
		self.local_mins.append(first_local_min)
		i = 1
		while i < len(agg_array)-1:
			if agg_array[i][0].value <= 2:
				if agg_array[i][0].value < agg_array[i-1][0].value and agg_array[i][0].value < agg_array[i+1][0].value:
					local_min = (agg_array[i][-1].pt2.value + agg_array[i][0].pt1.value)/2
					self.local_mins.append(local_min)
			i += 1

		##last_local_min = (agg_array[-1][-1].pt2.value + agg_array[-1][0].pt1.value)/2
		last_local_min = agg_array[-1][-1].pt2.value
		self.local_mins.append(last_local_min)

		self.areas = []

		for i, m in enumerate(self.local_mins[:-1]):
			a = Area(m, self.local_mins[i+1])
			self.areas.append(a)

	def print_mins(self):
		print(self.local_mins)

	## modifies intervals by deleting a key pt 
	def delete_key_pt(self, pt):
		##right at start add new interval at start
		if pt.value == self.interval_array[0].pt1.value:
			self.interval_array = self.interval_array[1:]
		##right at end add new interval at end
		elif pt.value == self.interval_array[-1].pt2.value:
			self.interval_array = self.interval_array[:-1]
		##don't delete if in the middle somewhere, too complicated
		else:
			pass

	
	## modifies intervals by adding another key pt possibly splitting an interval into 2
	def add_key_pt(self, pt):
		##right at start add new interval at start
		if pt.value < self.interval_array[0].pt1.value:
			new_range = Range(pt, self.interval_array[0].pt1, 0)
			self.interval_array.insert(0, new_range)
		##right at end add new interval at end
		elif pt.value > self.interval_array[-1].pt2.value:
			new_range = Range(self.interval_array[-1].pt2, pt, 0)
			self.interval_array.append(new_range)
		##insert somewhere in the middle
		else:
			spot = self.get_insertion_spot(pt)
			if spot == -1:
				pass
			else:
				(range1, range2) = Range.split(self.interval_array[spot], pt)
				self.interval_array[spot] = range1
				self.interval_array.insert(spot+1, range2)
		

	##finds all intervals that are covered by range r and adds amount to the interval values
	def update_interval_values(self, r, amount):
		low_val = 0
		high_val = 99999999999
		if r.type == "INC":
			val_low = r.pt1.value
			val_high = r.pt2.value
		elif r.type == "DESC":
			val_low = r.pt2.value
			val_high = r.pt1.value

		low_index = 0
		high_index = 0
		for i, interval in enumerate(self.interval_array):
			if interval.pt1.value == val_low:
				low_index = i
			elif interval.pt2.value == val_high:
				high_index = i

		for interval in self.interval_array[low_index:high_index + 1]:
			if interval.value + amount < 0:
				interval.value = 0
			else:
				interval.value += amount

	def pprint(self):
		print("Interval Array:")
		for r in self.interval_array:
			r.pprint()
		for m in self.local_mins:
			print(m)
	
	
	## return spot to insert the new pt into interval array
	## -1 means no insert neccesary
	def get_insertion_spot(self, new_pt):
		for i,r in enumerate(self.interval_array):	
			if new_pt.value == r.pt1.value or new_pt.value == r.pt2.value:
				return -1
			else:
				if r.is_between(new_pt.value):
					return i
