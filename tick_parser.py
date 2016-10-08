## adds ticks to table

from chart_tick import ChartTick
from db_manager import DBManager

class TickParser:
	def __init__(self, table_name, data):
		self.table_name = table_name
		self.data = data

		self.insert()
	
	def insert(self):
		db_manager = DBManager()
		for t in self.data:
			ct = ChartTick(db_manager, self.table_name, t)
			ct.save()
		db_manager.conn.commit()
		db_manager.conn.close()



