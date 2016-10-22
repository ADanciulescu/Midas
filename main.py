from poloniex_client import PoloniexClient
from db_manager import DBManager
from trade_simulator import TradeSimulator
from test_strategy import TestStrategy
from currency_trailer_strategy import CurrencyTrailerStrategy
from candle_table import CandleTable
from point_populator import PointPopulator
from simple_buyer_strategy import SimpleBuyerStrategy
from trend_fetcher import TrendFetcher
from trend_cutter import TrendCutter
from tools import date_to_timestamp
from two_avg_trend_strategy import TwoAvgTrendStrategy

##TODO: rename tick to candle
##TODO: move DBManager logic to candles and table classes

def main():
	##get_candle_data()
	##drop_table("eth_test")

	table_name_BTC_14400 = "USDT_BTC_1470628800_9999999999_14400"
	table_name_ETH_14400 = "USDT_ETH_1470628800_9999999999_14400"
	table_name_ethereum = "ethereum_table"
	##table_name = "USDT_BTC_1470628800_9999999999_300"
	##simulate_test_strategy(table_name_BTC_14400)
	##simulate_trailer_strategy(tn_reference = table_name_BTC_14400, tn_target = table_name_ETH_14400)
	##populate_sim_avg_points(table_name_ETH_14400, 10)
	##populate_sim_roc_points(table_name_ETH_14400)
	##populate_exp_avg_points(table_name_ETH_14400)
	simulate_two_trend_strategy(table_name_ethereum, table_name_ETH_14400)
	##grab_trend(table_name_ethereum, "ethereum", "08/2016", 3)
	##cut_trend(table_name_ETH_14400, table_name_ethereum)
	
	##print date_to_timestamp("2016-08-01")

## cut from the trend table to create a new trend table that matches the given candle table
def cut_trend(c_table_name, t_table_name):
	tc = TrendCutter(c_table_name, t_table_name)
	tc.create_cut_table()

##grabs google trends data
def grab_trend(table_name, keyword, date, num_months):
	tf = TrendFetcher(table_name, keyword, date, num_months)
	tf.fetch()

##drops table that matches the given table name
def drop_table(table_name):
	DBManager.drop_table(table_name)

def simulate_two_trend_strategy(trends_table, candle_table_name):
	strat = TwoAvgTrendStrategy(candle_table_name, trends_table)
	trade_sim = TradeSimulator(candle_table_name, strat)
	trade_sim.run()
	
def simulate_test_strategy(table_name):
	test_strat = TestStrategy()
	trade_sim = TradeSimulator(table_name, test_strat)
	trade_sim.run()

def simulate_buyer_strategy(table_name):
	strat = SimpleBuyerStrategy()
	trade_sim = TradeSimulator(table_name, strat)
	trade_sim.run()

def simulate_trailer_strategy(tn_reference, tn_target):
	strat = CurrencyTrailerStrategy(tn_reference, mode = CurrencyTrailerStrategy.EXP)
	trade_sim = TradeSimulator(tn_target, strat)
	trade_sim.run()


def populate_sim_avg_points(source_table_name, num_history_points):
	pt_table_name = source_table_name + PointPopulator.SIMPLE_AVG + "_" + str(num_history_points) 
	pp = PointPopulator(pt_table_name)
	pp.create_moving_avg_simple(num_history_points)

def populate_exp_avg_points(source_table_name):
	pt_table_name = source_table_name + PointPopulator.EXP_AVG 
	pp = PointPopulator(pt_table_name)
	pp.create_moving_avg_exp()

def populate_sim_roc_points(source_table_name):
	pt_table_name = source_table_name + PointPopulator.SIMPLE_ROC 
	pp = PointPopulator(pt_table_name)
	pp.create_roc()

##grabs candle data from poloniex and enters it into db
##data is entered into it's own table that is uniquely defined by the configurations(currenct pair, start, end etc.)
def get_candle_data():
	##configuration
	curr_ref = "USDT"
	curr_target = "ETH"
	start = 1470628800 ## aug 8 2016
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

main()
