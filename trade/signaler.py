## controls actual poloniex trading

from sig import Sig
from signal_table import SignalTable
from db_manager import DBManager
from bollinger_strategy import BollingerStrategy
from candle_fetcher import CandleFetcher 
from candle_table import CandleTable
import table_names
from time import time

class Signaler:
	
	HISTORY_LENGTH = 2592000 ## how long of a history to use when producing signals = 1 months in seconds

	def __init__(self):
		self.signal_table_names = [] ## stores signal_table_names
		self.new_signals_array = [] ## stores arrays of new signals

	def run(self, to_print = True):
		self.update_all_signals()
		self.push_to_db()
		self.handle_new_signals()
		if to_print:
			self.print_all_signals()
	
	##push the newly created signals to db
	def push_to_db(self):
		for i, tn in enumerate(self.signal_table_names):
			if not DBManager.exists_table(tn):
				st = SignalTable(tn)
				st.save()
			
			for s in self.new_signals_array[i]:
				s.save()
			dbm = DBManager.get_instance()
			dbm.save_and_close()

				
	## update new_singals_array with any new signals
	def update_all_signals(self):
		CandleFetcher.update_all()
		
		##for each candle table, compute signal table name and get new signals
		for tn in table_names.trader_tables:
			signal_table_name = tn.replace("CANDLE", "SIGNAL")
			self.signal_table_names.append(signal_table_name)
			self.new_signals_array.append(self.get_new_signals(tn))
	
	##prints signals from all currencies
	def print_all_signals(self):
		for tn in self.signal_table_names:
			signals = SignalTable.get_signal_array(tn)
			print "******************************************************************************"
			print tn
			for s in signals[-10:]:
				s.pprint()
			print "******************************************************************************"

	## analyzes a table and returns possible new_signal
	def get_new_signals(self, table_name):
		cur_date = int(time())
		signal_table_name = table_name.replace("CANDLE", "SIGNAL")
		last_date = 0

		if DBManager.exists_table(signal_table_name):
			last_date = SignalTable.get_last_date(signal_table_name)
			

		##cut the candle table to get one of a more manageable size
		cut_table_name = CandleFetcher.cut_table(table_name, cur_date - Signaler.HISTORY_LENGTH)
		candles = CandleTable.get_candle_array(table_name)
		
		new_signals = []

		##run a bollinger strategy on the candles and store the resulting operations returned
		strat = BollingerStrategy(table_name, set_default = True)
		for i in range(len(candles)):
			o = strat.decide(i, 0)
			sig = Sig(signal_table_name, candles[i].date, o.amount, candles[i].close, o.op)
			
			##if after last_date it means the signal is new
			if sig.date > last_date:
				new_signals.append(sig)

		##delete created table when done
		DBManager.drop_table(cut_table_name)
		return new_signals
			
