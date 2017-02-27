## used to grab snapshots from poloniex and insert into db
from snap import Snap
from snap_order import SnapOrder
from snap_table import SnapTable
from snap_order_table import SnapOrderTable
from db_manager import DBManager
from poloniex import Poloniex
import time

class SnapFetcher:

	NUM_ORDER = 3 ##fetch NUM_ORDER sell orders and NUM_ORDER buy orders for each snap

	def __init__(self, snap_table_name):
		self.snap_tn = snap_table_name
		self.snap_order_tn = SnapOrderTable.create_name(self.snap_tn)
		self.polo = Poloniex.get_instance()

		##create tables if they don't already exist
		if not DBManager.exists_table(self.snap_tn):
			st = SnapTable(self.snap_tn)
			st.save()
		if not DBManager.exists_table(self.snap_order_tn):
			st = SnapOrderTable(self.snap_order_tn)
			st.save()

	##keeps fetching snaps continously until process is killed
	def run(self):
		while(True):
			self.fetch_snap()
			time.sleep(1)
	
	##fetches one snap
	def fetch_snap(self):
		cur_time = int(time.time())

		curr_pair = SnapTable.get_currency_pair(self.snap_tn)
		
		##create snap
		s = Snap(self.snap_tn, cur_time)
		s.save()

		##create all the snap orders corresponding to snap
		polo_data = self.polo.returnOrderBook(curr_pair)
		
		bids = polo_data["bids"]
		type = "bid"
		for a in bids[:SnapFetcher.NUM_ORDER]:
			rate = float(a[0])
			amount = float(a[1])
			so = SnapOrder(self.snap_order_tn, cur_time, amount, rate, type)
			so.save()
		
		asks = polo_data["asks"]
		type = "ask"
		for a in asks[:SnapFetcher.NUM_ORDER]:
			rate = float(a[0])
			amount = float(a[1])
			so = SnapOrder(self.snap_order_tn, cur_time, amount, rate, type)
			so.save()


	


