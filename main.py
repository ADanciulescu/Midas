from poloniex_client import PoloniexClient
from poloniex import Poloniex
from db_manager import DBManager
from trade_simulator import TradeSimulator
from test_strategy import TestStrategy
from currency_trailer_strategy import CurrencyTrailerStrategy
from candle_table import CandleTable
from candle_fetcher import CandleFetcher
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
from oscil_strategy import OscilStrategy
from random_strategy import RandomStrategy
from hold_strategy import HoldStrategy
from signaler import Signaler
from sig import Sig
from parameter_optimizer import ParameterOptimizer
from order_maker import OrderMaker
from emailer import Emailer
import table_names
import time


##TODO: keep testing with more data and keep adjusting parameters
##TODO: buy btc
##TODO: write automated platform
##TODO: setup a aws server
##TODO: keep thinking of possible biases
##TODO: Fix limit on tradesimulator
##lookinto fixing stddev_adjust, possibly sell/buy more first time(after num_past...)
## verify stddev and avg are calculated properly( no off by one errors)

def main():
	##test = Sig("tn", 1451793600, "BTC", 1.1, 42, "BUY")
	##e = Emailer()
	##e.email_signal(test)
	##om = OrderMaker([])
	##om.get_top_buy_price("USDT_BTC")
	DBManager.drop_matching_tables("SIGNAL")
	##p = Poloniex()
	##signaler = Signaler()
	##signaler.run()
	##signaler.print_all_signals()
	##CandleFetcher.update_all()
	##CandleFetcher.fetch_candles_after_date("BTC", date_to_timestamp("2016-1-1"), 1800)
	##CandleFetcher.fetch_candles_after_date("ETH", date_to_timestamp("2016-1-1"), 1800)
	##CandleFetcher.fetch_candles_after_date("XMR", date_to_timestamp("2016-1-1"), 1800)
	##CandleFetcher.fetch_candles_after_date("ZEC", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("NXT", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("STR", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("LTC", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("ETC", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("DASH", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("REP", date_to_timestamp("2016-1-1"), 14400)
	##CandleFetcher.fetch_candles_after_date("LTC", date_to_timestamp("2016-1-1"), 7200)
	##CandleFetcher.fetch_candles_after_date("ETC", date_to_timestamp("2016-1-1"), 7200)
	##CandleFetcher.fetch_candles_after_date("REP", date_to_timestamp("2016-1-1"), 7200)
	##CandleFetcher.fetch_candles_after_date("DASH", date_to_timestamp("2016-1-1"), 7200)
	##CandleFetcher.fetch_candles_after_date("XMR", date_to_timestamp("2016-1-1"), 14400)
	
	##CandleFetcher.cut_table(table_names.BTC_7200, date_to_timestamp("2016-1-1"), date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.ETH_7200, date_to_timestamp("2016-1-1"), date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.XMR_7200, date_to_timestamp("2016-1-1"), date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.XRP_7200, date_to_timestamp("2016-1-1"), date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.DASH_7200, date_to_timestamp("2016-1-1"), date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.LTC_7200, date_to_timestamp("2016-1-1"), date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.XRP_14400, date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.LTC_14400, date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.ETC_14400, date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.DASH_14400, date_to_timestamp("2016-6-1"))
	##CandleFetcher.cut_table(table_names.REP_14400, date_to_timestamp("2016-6-1"))

	##populate_exp_avg_points(table_name_ETH_14400)
	##grab_trend_all(trend_name_XMR, "XMR")
	##cut_trend(table_name_ETH_14400, table_name_ETH)

	##DBManager.drop_matching_tables("OSCIL")
	##simulate_oscil_strategy(table_names.BIG_HALF1_14400)
	##simulate_bollinger_strategy(table_names.BIG_HALF2_14400)
	##simulate_bollinger_strategy(table_names.BIG_HALF2_14400)
	##simulate_hold_strategy(table_names.SMALL_HALF2_14400)
	##simulate_bollinger_strategy(tn_HALF_7200)
	##simulate_hold_strategy(tn_7200)
	##simulate_bollinger_strategy(tn2_HALF_7200)
	##simulate_bollinger_strategy(tn1_HALF_7200)
	##tn2_HALF_1800 = [table_names.XRP_HALF_1800, table_names.LTC_HALF_1800, table_names.ETC_HALF_1800, table_names.DASH_HALF_1800, table_names.REP_HALF_1800]
	##simulate_bollinger_strategy([table_names.BTC_HALF, table_names.ETH_HALF, table_names.XMR_HALF])
	##simulate_bollinger_strategy([table_names.BTC_HALF_7200, table_names.ETH_HALF_7200, table_names.XMR_HALF_7200])
	##simulate_bollinger_strategy(tn2_7200)
	##simulate_bollinger_strategy([table_names.XMR_HALF])
	
	optimize(table_names.BIG_HALF2_7200)
	
	##simulate_bollinger_strategy([table_names.XRP_HALF, table_names.LTC_HALF, table_names.ETC_HALF, table_names.REP_HALF, table_names.DASH_HALF])
	
	
	##present_bollinger(table_names.ETC_14400)
	##present_bollinger(table_names.DASH_14400)

	##simulate(table_name_BTC_14400)
	##simulate(table_name_LTC_14400)

## optimize parameters
def optimize(table_name_array):
	po = ParameterOptimizer(table_name_array)
	po.optimize_bollinger()

def simulate_oscil_strategy(candle_table_name_array):
	strat_array = []
	for tn in candle_table_name_array:
		strat = OscilStrategy(tn)
		strat_array.append(strat)
	trade_sim = TradeSimulator(candle_table_name_array, strat_array, to_log = True)
	trade_sim.run()

def simulate_bollinger_strategy(candle_table_name_array):
	strat_array = []
	for tn in candle_table_name_array:
		strat = BollingerStrategy(tn, set_default = True)
		strat_array.append(strat)
	trade_sim = TradeSimulator(candle_table_name_array, strat_array, to_log = True)
	trade_sim.run()

def simulate_hold_strategy(candle_table_name_array):
	strat_array = []
	for tn in candle_table_name_array:
		strat = HoldStrategy(tn)
		strat_array.append(strat)
	trade_sim = TradeSimulator(candle_table_name_array, strat_array, to_log = True)
	trade_sim.run()

def present_bollinger(candle_table_name):
	candles = CandleTable.get_candle_array(candle_table_name)
	strat = BollingerStrategy(candles)
	print "# of stddev from mean: ", strat.get_present_bollinger_diff()

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

def simulate_random_strategy(candle_table_name):
	candles = CandleTable.get_candle_array(candle_table_name)
	strat = RandomStrategy(candles)
	trade_sim = TradeSimulator(candle_table_name, candles, strat)
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

