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
from manual_trend_strategy import ManualTrendStrategy
from manual_attribute_strategy import ManualAttributeStrategy
from scipy_trend_model_strategy import ScipyTrendModelStrategy
from scipy_candle_model_strategy import ScipyCandleModelStrategy
from neural_trend_model import NeuralTrendModel
from neural_candle_model import NeuralCandleModel
from bollinger_strategy import BollingerStrategy
from random_strategy import RandomStrategy
import time
import table_names

##TODO: investigate modifying candle_length to something smaller than 14400
##TODO: look into finding a parameter optimizer
##TODO: keep testing with more data and keep adjusting parameters
##TODO: buy btc
##TODO: write automated platform
##TODO: setup a aws server
##TODO: keep thinking of possible biases

def main():
	

	##get_candle_data("ETH")
	##get_candle_data("ETH")
	##get_candle_data("XRP")
	##get_candle_data("LTC")
	##get_candle_data("ETC")
	##get_candle_data("XMR")
	##get_candle_data("DASH")
	##get_candle_data("REP")
	##table_name = "USDT_BTC_1475280000_9999999999_300"
	##simulate_test_strategy(table_name_BTC_14400)
	##simulate_trailer_strategy(tn_reference = table_name_BTC_14400, tn_target = table_name_ETH_14400)
	##populate_sim_avg_points(table_name_ETH_14400, 10)
	##populate_sim_roc_points(table_name_ETH_14400)
	##populate_exp_avg_points(table_name_ETH_14400)
	##grab_trend_all(table_name_ripple, "ripple")
	##grab_trend_all(trend_name_ETH, "ETH")
	##grab_trend_all(trend_name_BTC, "BTC")
	##grab_trend_all(trend_name_XMR, "XMR")
	##cut_trend(table_name_ETH_14400, table_name_ETH)

	
	##nm = NeuralCandleModel("volume")
	##nm.cross_validate(table_name_BTC_14400)
	##nm.train_model(CandleTable.get_candle_array(table_name_XMR_14400))
	##nm.train_model(CandleTable.get_candle_array(table_name_ETH_14400))
	##nm.test_model(CandleTable.get_candle_array(table_name_XMR_14400))
	##train_candles = CandleTable.get_candle_array_by_date(table_name_BTC_14400, date_high = 1482508800)
	##nm.train_model(train_candles)
	##sim_candles = CandleTable.get_candle_array_by_date(table_name_XMR_14400, date_low = 1482508800)
	##sim_candles = CandleTable.get_candle_array(table_name_BTC_14400)
	##simulate_scipy_candle_strategy(table_name_BTC_14400, sim_candles, nm)	

	##simulate_manual_attribute_strategy(table_name_BTC_14400, "volume")

	##present_bollinger(table_names.ETH_14400)
	simulate_bollinger_strategy(table_names.ETH_14400)
	##simulate_bollinger_strategy(table_name_ETH4_14400)
	##simulate_bollinger_strategy(table_name_XMR4_14400)
	##simulate_bollinger_strategy(table_name_XRP4_14400)
	##simulate_bollinger_strategy(table_name_LTC4_14400)
	##simulate_bollinger_strategy(table_name_ETH2_14400)
	#simulate_bollinger_strategy(table_name_ETC_14400)
	##simulate_bollinger_strategy(table_name_ETC2_14400)
	##simulate_bollinger_strategy(table_name_XMR_14400)
	##simulate_bollinger_strategy(table_name_XMR2_14400)
	##simulate_bollinger_strategy(table_name_LTC_14400)
	##simulate_bollinger_strategy(table_name_LTC2_14400)
	##simulate_random_strategy(table_name_ETH2_14400)
	##simulate_bollinger_strategy(table_name_LTC_14400)
	##simulate_bollinger_strategy(table_name_ETC_14400)

	##simulate(table_name_BTC_14400)
	##simulate(table_name_LTC_14400)


##find best parameter setting
def simulate(candle_table_name):
	candles = CandleTable.get_candle_array(candle_table_name)
	
	past_sell = 0
	while past_sell <= 10:
		print "******************************************************************************************"
		print "PAST_SELL: ", past_sell
		print ""
		strat = BollingerStrategy(candles, num_past_sell = past_sell)
		trade_sim = TradeSimulator(candle_table_name, candles, strat)
		trade_sim.run()
		print "******************************************************************************************"
		past_sell += 2
	

def present_bollinger(candle_table_name):
	candles = CandleTable.get_candle_array(candle_table_name)
	strat = BollingerStrategy(candles)
	print strat.get_present_bollinger_diff()

def simulate_random_strategy(candle_table_name):
	candles = CandleTable.get_candle_array(candle_table_name)
	strat = RandomStrategy(candles)
	trade_sim = TradeSimulator(candle_table_name, candles, strat)
	trade_sim.run()


def simulate_bollinger_strategy(candle_table_name):
	candles = CandleTable.get_candle_array(candle_table_name)
	strat = BollingerStrategy(candles)
	trade_sim = TradeSimulator(candle_table_name, candles, strat)
	trade_sim.run()

def simulate_scipy_trend_strategy(candle_table_name, trend_table_name, model):
	strat = ScipyModelStrategy(candle_table_name, trend_table_name, model)
	trade_sim = TradeSimulator(candle_table_name, strat)
	trade_sim.run()

def simulate_scipy_candle_strategy(candle_table_name, sim_candles, model):
	strat = ScipyCandleModelStrategy(sim_candles, model)
	trade_sim = TradeSimulator(candle_table_name, sim_candles, strat)
	trade_sim.run()

def simulate_two_trend_strategy(trends_table, candle_table_name):
	strat = TwoAvgTrendStrategy(candle_table_name, trends_table)
	trade_sim = TradeSimulator(candle_table_name, strat)
	trade_sim.run()
	
def simulate_manual_trend_strategy(candle_table_name):
	strat = ManualTrendStrategy(candle_table_name)
	trade_sim = TradeSimulator(candle_table_name, strat)
	trade_sim.run()

def simulate_manual_attribute_strategy(candle_table_name, attr_name):
	sim_candles = CandleTable.get_candle_array(candle_table_name)
	strat = ManualAttributeStrategy(sim_candles, attr_name)
	trade_sim = TradeSimulator(candle_table_name, sim_candles, strat)
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


##grabs candle data from poloniex and enters it into db
##data is entered into it's own table that is uniquely defined by the configurations(currenct pair, start, end etc.)
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


##drops table that matches the given table name
def drop_table(table_name):
	DBManager.drop_table(table_name)

## cut from the trend table to create a new trend table that matches the given candle table
def cut_trend(c_table_name, t_table_name):
	tc = TrendCutter(c_table_name, t_table_name)
	tc.create_cut_table()

##grabs google trends data
def grab_trend(table_name, keyword, date, num_months):
	tf = TrendFetcher(table_name, keyword, date, num_months)
	tf.fetch()

##grabs google trends data for multiple months
def grab_trend_all(table_name, keyword):
	##grab_trend(table_name, keyword, "/2015", 3)
	##time.sleep(3)
	##grab_trend(table_name, keyword, "01/2016", 3)
	##time.sleep(3)
	##grab_trend(table_name, keyword, "04/2016", 3)
	##time.sleep(3)
	##grab_trend(table_name, keyword, "07/2016", 3)
	grab_trend(table_name, keyword, "08/2016", 3)
	time.sleep(3)
	grab_trend(table_name, keyword, "11/2016", 3)


def populate_sim_avg_points(source_table_name, num_history_points):
	pp = PointPopulator(source_table_name)
	pp.create_moving_avg_simple(num_history_points)

def populate_exp_avg_points(source_table_name):
	pp = PointPopulator(source_table_name)
	pp.create_moving_avg_exp()

def populate_sim_roc_points(source_table_name):
	pp = PointPopulator(source_table_name)
	pp.create_roc()


main()

