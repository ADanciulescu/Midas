##fetches candle data and completes a large candle table for each currency

from poloniex_client import PoloniexClient
from tools import timestamp_to_date
from db_manager import DBManager
from candle_table import CandleTable
from time import time

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
