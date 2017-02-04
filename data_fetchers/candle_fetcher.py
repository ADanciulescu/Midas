##fetches candle data and completes a large candle table for each currency

from poloniex

class CandleFetcher():
	
	def get_candle_data(curr_target):
		##configuration
		curr_ref = "USDT"
		##curr_target = "BTC"
		##start = 1451606400 ## Jan 01 2016
		##end = 1459468800## Apr 1 2016
		##start = 1459468800## Apr 1 2016
		##end = 1467331200 ## july 01 2016
		##start = 1467331200 ## july 01 2016
		##end =  1475280000## oct 01 2016 
		start = 1475280000 ## aug 8 2016
		end = 9999999999 ## present
		period = 14400 ## in seconds
		
		table_name = CandleTable.calc_table_name(curr_ref, curr_target, start, end, period)
		
		##if exists drop firt and recreate
		if DBManager.exists_table(table_name):
			print "table with same configuration already exists, deleting it and rebuilding..."
			drop_table(table_name)
		ct = CandleTable(curr_ref, curr_target, start, end, period)
		ct.save()
		pc = PoloniexClient(table_name)
		pc.populate_candle_db(curr_ref, curr_target, start, end, period)
