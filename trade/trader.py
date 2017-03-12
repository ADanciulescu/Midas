##runs in a loop and trades

from db_manager import DBManager
from signaler import Signaler
from candle_table import CandleTable
from order_maker import OrderMaker
import table_names
import time

class Trader:

	CLASSIC = "classic"
	PREORDER = "preorder"

	def __init__(self, mode):
		##DBManager.drop_matching_tables("SIGNAL")
		self.signaler = Signaler(table_names.short_term_tables, to_print = False, to_email = False)
		self.period =  float(CandleTable.get_period(table_names.short_term_tables[0]))
		self.order_maker = OrderMaker()
		self.mode = mode

	def run(self):
		print("Starting Trader")
		while(True):
			secs_last_run = CandleTable.get_last_date(table_names.short_term_tables[0])
			secs_cur = time.time()
			
			##print secs_cur-secs_last_run
			if(secs_cur-secs_last_run) > (self.period+1):
				print("***********************************SIGNALS*********************************************")
				self.order_maker.update_balances()
				self.signaler.update(self.order_maker.is_owned)
				new_signals_array = self.signaler.new_signals_array
				self.handle_new_currency_signals(new_signals_array)
				for i in range(len(table_names.short_term_tables)):
					print("last operation was: " , self.signaler.strat_array[i].last)

	##perform buys/sells depending on last signal
	def handle_new_currency_signals(self, new_signals_array):
		for i, s in enumerate(new_signals_array):
			last_signal = s[-1]
			last_signal.pprint()
			if self.mode == Trader.CLASSIC:
				self.order_maker.handle_signal_classic(last_signal)	
			else:
				operating_range = (self.signaler.strat_array[i].floor, self.signaler.strat_array[i].ceiling)
				self.order_maker.handle_signal_preorder(last_signal, operating_range)	
			



