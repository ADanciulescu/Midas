##runs in a loop and trades

from db_manager import DBManager
from signaler import Signaler
from candle_table import CandleTable
from order_maker import OrderMaker
from order_updater import OrderUpdater
from scheduler import Scheduler
from task import Task
import table_names
import time

class Trader:

	CLASSIC = "classic"
	PREORDER = "preorder"

	def __init__(self, mode):
		self.mode = mode
		self.order_updater = OrderUpdater()
		self.scheduler = Scheduler()
		self.signaler = Signaler(table_names.short_term_tables, to_print = False, to_email = False)
		self.order_maker = OrderMaker(self.order_updater, self.scheduler)

	def run(self):
		print("Starting Trader")
		signal_task = Task(self.grab_new_signals, 0, ())
		self.scheduler.schedule_task(signal_task)
		update_task = Task(self.order_updater.update_orders, 5, ())
		self.scheduler.schedule_task(update_task)
		self.scheduler.run()

	def grab_new_signals(self):
		period =  float(CandleTable.get_period(table_names.short_term_tables[0]))
		last_time = CandleTable.get_last_date(table_names.short_term_tables[0])
		cur_time = time.time()
		if(cur_time-last_time) > (period+1):
			print("***********************************SIGNALS*********************************************")
			self.signaler.update(self.order_updater.sym_infos)
			new_signals_array = self.signaler.new_signals_array
			self.handle_new_currency_signals(new_signals_array)
			
			sym_infos = self.order_updater.sym_infos
			for key, value in sym_infos.items():
				print("last operation was: " , value.is_owned)

		return Task.CONTINUE

	##perform buys/sells depending on last signal
	def handle_new_currency_signals(self, new_signals_array):
		for i, s in enumerate(new_signals_array):
			last_signal = s[-1]
			last_signal.pprint()
			if self.mode == Trader.CLASSIC:
				self.order_maker.handle_signal_classic(last_signal)	
			##else:
				##operating_range = (self.signaler.strat_array[i].floor, self.signaler.strat_array[i].ceiling)
				##self.order_maker.handle_signal_preorder(last_signal, operating_range)	
			



