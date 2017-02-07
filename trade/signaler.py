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
	
	HISTORY_LENGTH = 5184000 ## how long of a history to use when producing signals = 2 months in seconds

	def __init__(self):
		pass

	##prints signals from all currencies
	def print_all_signals(self):
		CandleFetcher.update_all()

		##run get_currency_signals for all the major currencies
		for tn in table_names.trader_tables:
			signals = self.get_currency_signals(tn)
			
			##print the last 10 signals
			print "******************************************************************************"
			for s in signals[-10:]:
				s.pprint()
			print "******************************************************************************"

	## analyzes a table and returns possible signal
	def get_currency_signals(self, table_name):
		
		##prepare a signal table to add signals to
		signal_table_name = table_name.replace("CANDLE", "SIGNAL")
		if DBManager.exists_table(signal_table_name):
			DBManager.drop_table(signal_table_name)

		st = SignalTable(signal_table_name)
		st.save()

		cur_date = int(time())
		##cut the table to get one of a more manageable size
		cut_table_name = CandleFetcher.cut_table(table_name, cur_date - Signaler.HISTORY_LENGTH)
		candles = CandleTable.get_candle_array(table_name)
		
		strat = BollingerStrategy(table_name)

		##run a bollinger strategy on the candles and store the resulting operations returned
		signals = []

		for i in range(len(candles)):
			o = strat.decide(i, 0)
			sig = Sig(signal_table_name, candles[i].date, o.amount, candles[i].close, o.op)
			sig.save()
			signals.append(sig)
		dbm = DBManager.get_instance()
		dbm.save_and_close()	
		return signals
			
