##runs in a loop and trades

from signaler import Signaler
from candle_table import CandleTable
from order_maker import OrderMaker
import table_names
import time

class Trader:

	def __init__(self):
		self.signaler = Signaler(table_names.short_term_tables, to_print = False, to_email = False)
		self.period =  float(CandleTable.get_period(table_names.short_term_tables[0]))
		self.order_maker = OrderMaker()

	def run(self):
		while(True):
			secs_last_run = CandleTable.get_last_date(table_names.short_term_tables[0])
			secs_cur = time.time()
			
			##print secs_cur-secs_last_run
			if(secs_cur-secs_last_run) > (self.period+90):
				self.signaler.update()
				new_signals_array = self.signaler.new_signals_array
				print "***********************************SIGNALS*********************************************"
				for ns in new_signals_array:
					self.handle_new_currency_signals(ns)

	##perform buys/sells depending on last signal
	def handle_new_currency_signals(self, signal_array):
		if len(signal_array) > 0:
			last_signal = signal_array[-1]
		 	last_signal.pprint()
			self.order_maker.handle_signal(last_signal)	
			



