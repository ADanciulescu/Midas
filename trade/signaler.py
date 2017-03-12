## controls actual poloniex trading

from sig import Sig
from signal_table import SignalTable
from db_manager import DBManager
from bollinger_strategy import BollingerStrategy
from short_term_strategy import ShortTermStrategy
from candle_fetcher import CandleFetcher 
from candle_table import CandleTable
from emailer import Emailer
import table_names
from time import time

class Signaler:
	
	HISTORY_LENGTH = 2592000 ## how long of a history to use when producing signals = 1 months in seconds

	def __init__(self, trader_tables, to_print = True, to_email = False):
		self.signal_table_names = [] ## stores signal_table_names
		self.new_signals_array = [] ## stores arrays of new signals
		self.to_print = to_print
		self.to_email = to_email
		self.stddev_array = [] ##specifically used for bollinger strategy
		self.trader_tables = trader_tables
		self.strat_array = []
		self.setup()
		self.is_owned = {} ## array holding info about whether a currency is owned(true) or not(false) 
	
	##setup before it runs
	## populates signal_table_names
	def setup(self):
		for tn in self.trader_tables:
			strat = ShortTermStrategy(tn, is_simul = False, to_print = False)
			self.strat_array.append(strat)
			signal_table_name = tn.replace("CANDLE", "SIGNAL_" + strat.get_name())
			self.signal_table_names.append(signal_table_name)
	
	##is_owned is used to determine what currencies are available to be sold/bought(passed into corresponding Strategy to make correct decision)
	## updates signaler with new signals
	def update(self, is_owned):
		self.is_owned = is_owned 
		self.new_signals_array = []
		self.update_all_signals()
		self.push_to_db()

	def handle_new_signals(self):
		if self.to_email:
			emailer = Emailer()
			for a in self.new_signals_array:
				if len(a) > 0:
					sig = a[-1]
					if sig.type == Sig.BUY or sig.type == Sig.SELL:
						emailer.email_signal(sig)

	##push the newly created signals to db
	def push_to_db(self):
		for i, tn in enumerate(self.signal_table_names):
			if not DBManager.exists_table(tn):
				st = SignalTable(tn)
				st.save()
			
			for s in self.new_signals_array[i]:
				s.save()

				
	## update new_singals_array with any new signals
	def update_all_signals(self):
		
		##update tables with new data
		CandleFetcher.update_tables_imperative(self.trader_tables, self.is_owned)
		
		
		##for each candle table, compute signal table name and get new signals
		for i in range(len(self.trader_tables)):
			new_signals = self.get_new_signals(i)
			self.new_signals_array.append(new_signals)

		if self.to_print:
			self.print_new_signals()

	def print_new_signals(self):
		for i,tn in enumerate(self.signal_table_names):
			print(tn)
			for s in self.new_signals_array[i]:
				s.pprint()

	
	##prints signals from all currencies
	def print_all_signals(self):
		for i,tn in enumerate(self.signal_table_names):
			signals = SignalTable.get_signal_array(tn)
			print("******************************************************************************")
			print(tn)
			for s in signals[-10:]:
				s.pprint()
			print(("# of stddev from mean: ", self.stddev_array[i]))
	
	##find index of first candle with date bigger than last_date
	def find_new_candle_index(self, candles, last_date):
		len_candles = len(candles)
		i = len_candles - 1
		while i >= 0:
			if candles[i].date < last_date:
				return i + 1 
			i -= 1
		return 0	


	## analyzes a table and returns possible new_signal
	def get_new_signals(self, tn_index):

		tn = self.trader_tables[tn_index]
		signal_tn = self.signal_table_names[tn_index]

		cur_date = int(time())
		last_date = SignalTable.get_last_date(signal_tn)
		period = float(CandleTable.get_period(tn))
		
		##cut the candle table to get one of a more manageable size
		cut_table_name = CandleFetcher.cut_table(tn, int(cur_date - 5*ShortTermStrategy.DATA_PAST*period))
		candles = CandleTable.get_candle_array(cut_table_name)

		##new_candle_index = self.find_new_candle_index(candles, last_date)
		
		new_signals = []

		##run a strategy on the candles and store the resulting operations returned
		strat = self.strat_array[tn_index]
		sym = SignalTable.get_sym(self.signal_table_names[tn_index])
		strat.update_state(candles, self.is_owned[sym])
	
		##i = new_candle_index
		##while i < len(candles):
		i = len(candles) - 1
		o = strat.decide(i, 0)	
		sig = Sig(signal_tn, candles[i].date, SignalTable.get_sym(signal_tn), o.amount, candles[i].close, o.op)
		new_signals.append(sig)	
		##i += 1

		##delete created table when done
		DBManager.drop_table(cut_table_name)
		return new_signals
			
