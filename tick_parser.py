## adds ticks to table

from chart_tick import ChartTick

class TickParser:
	def __init__(self, table_name, data):
		self.table_name = table_name
		self.data = data

		self.insert()
	
	def insert(self):
		for t in self.data:
			ct = ChartTick(self.table_name, t)
			ct.save()



