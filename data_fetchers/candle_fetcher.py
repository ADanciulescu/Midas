##fetches candle data and completes a large candle table for each currency

from poloniex_client import PoloniexClient
from tools import timestamp_to_date
from db_manager import DBManager
from candle_table import CandleTable
from candle import Candle
from time import time
import table_names

class CandleFetcher():

	FETCH_WINDOW_LENGTH = 7776000 ##3 months in seconds

	
	## fetches candle data for the given currency between the 2 dates and adds it to the big candle table
	## big candle table is uniquely defined by currency and period
	@staticmethod
	def get_candle_data(curr_target, date_start, date_end, period):
		print "Adding ", curr_target, " candle data between: ", timestamp_to_date(date_start), " ---- ", timestamp_to_date(date_end)  
		##configuration
		curr_ref = "USDT"
		##curr_target = "BTC"
		##start = 1451606400 ## Jan 01 2016
		##end = 1459468800## Apr 1 2016
		##start = 1459468800## Apr 1 2016
		##end = 1467331200 ## july 01 2016
		##start = 1467331200 ## july 01 2016
		##end =  1475280000## oct 01 2016 
		##start = 1475280000 ## aug 8 2016
		##end = 9999999999 ## present
		##period = 14400 ## in seconds
		
		##table_name = CandleTable.calc_table_name(curr_ref, curr_target, start, end, period)
		table_name = "CANDLE_" + curr_ref + "_" + curr_target + "_" + str(period)

		if not DBManager.exists_table(table_name):
			ct = CandleTable(curr_ref, curr_target, date_start, date_end, period, table_name)
			ct.save()

		pc = PoloniexClient(table_name)
		pc.populate_candle_db(curr_ref, curr_target, date_start, date_end, period)
		
	## adds everything from date_start to present to the given currency table
	## makes repeated calls to get_candle_data to fetch the data in 3 month chunks
	@staticmethod
	def fetch_candles_after_date(curr_target, orig_date_start, period):
		date_start = orig_date_start
		cur_time = time()
		while(date_start < cur_time):
			date_end = date_start + CandleFetcher.FETCH_WINDOW_LENGTH
			CandleFetcher.get_candle_data(curr_target, date_start, date_end, period)
			date_start = date_end
	
	##cuts a big candle table up and creates a currency table that only contains candles between 2 given dates
	##returns new candle_table name
	@staticmethod
	def cut_table(orig_table_name, date_start, date_end):
		print "Cutting table: ", orig_table_name, " candle data between: ", timestamp_to_date(date_start), " ---- ", timestamp_to_date(date_end)  
		
		##create new table
		curr_ref = CandleTable.get_ref_currency(orig_table_name)	
		curr_target = CandleTable.get_target_currency(orig_table_name)	
		period = CandleTable.get_period(orig_table_name)
		new_table = CandleTable(curr_ref, curr_target, date_start, date_end, period)
		new_table_name = new_table.table_name
		
		if DBManager.exists_table(new_table_name):
			DBManager.drop_table(new_table_name)
		
		new_table.save()

		
		##populate new table with candles from orig_table that lie between the 2 dates
		dbm = DBManager()
		candle_array = CandleTable.get_candle_array_by_date(orig_table_name, date_start, date_end)
		for c in candle_array:
			new_c = Candle(dbm, new_table_name, c.date, c.high, c.low, c.open, c.close, c.volume, c.quoteVolume, c.weightedAverage)
			new_c.save()
		dbm.conn.commit()
		dbm.conn.close()

		return new_table_name

	##updates the big tables for all the currencies with any new candles
	@staticmethod
	def update_all():
		for tn in table_names.complete_tables:
			last_date_updated = CandleTable.get_last_date(tn)
			target_curr = CandleTable.get_target_currency(tn)
			period = CandleTable.get_period(tn)
			CandleFetcher.fetch_candles_after_date(target_curr, last_date_updated, period)
		

			
