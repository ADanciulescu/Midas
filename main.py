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
from short_term_strategy import ShortTermStrategy
from signaler import Signaler
from sig import Sig
from parameter_optimizer import ParameterOptimizer
from order_maker import OrderMaker
from order_table import OrderTable
from emailer import Emailer
from snap_fetcher import SnapFetcher
from snap_table import SnapTable
from snap_order_table import SnapOrderTable
from normal_strategy import NormalStrategy
from trader import Trader
import table_names
import time
import threading

##TODO: keep testing with more data and keep adjusting parameters
##TODO: buy btc
##TODO: write automated platform
##TODO: setup a aws server
##TODO: keep thinking of possible biases
##TODO: Fix limit on tradesimulator
##lookinto fixing stddev_adjust, possibly sell/buy more first time(after num_past...)
## verify stddev and avg are calculated properly( no off by one errors)

HALF_DAY = 43200

def main():
	test = Sig("tn", 1451793600, "BTC", 1.1, 42, "BUY")

	##DBManager.drop_matching_tables("SIGNAL")
	##signaler = Signaler(table_names.short_term_tables)
	##signaler.update()

	##OrderTable.create_tables()
	##om = OrderMaker()
	##om.slow_sell("XRP", 1, sell_all = True)
	##om = OrderMaker()
	##om.slow_sell("ETH", 1, sell_all = True)
	
	##OrderMaker.get_last_trade_rate("USDT_BTC")
	##DBManager.drop_matching_tables("SIGNAL")
	##CandleFetcher.fetch_candles_after_date("XRP", date_to_timestamp("2016-6-1"), 300)
	##CandleFetcher.update_tables(table_names.short_term_tables)
	trader = Trader(Trader.CLASSIC)
	trader.run()

	##while(True):
		##print(time.time())
		##CandleFetcher.update_tables_imperative([table_names.BTC_300],[True])
		##time.sleep(1)

	##DBManager.drop_matching_tables("SNAP")
	##print threading.get_ident()
	##sf = SnapFetcher("SNAP_USDT_BTC_100")
	##sf.run()

	##SnapTable.delete_rows("SNAP_USDT_BTC_100")
	##SnapOrderTable.delete_rows("SNAP_ORDER_USDT_BTC_100")

	##OrderMaker.slow_sell("ETC", 60)
	##OrderMaker.update_orders()
	##OrderMaker.place_buy_order("NXT", 0.01)

	##CandleFetcher.fetch_candles_after_date("BTC", date_to_timestamp("2017-3-1"), 300)
	##e = Emailer()
	##e.email_signal(test)
	##om = OrderMaker([])
	##om.get_top_buy_price("USDT_BTC")
	##DBManager.drop_matching_tables("SNAP")
	##p = Poloniex()
	##signaler = Signaler(to_email = False, to_print = True)
	##signaler.run()
	##signaler.print_all_signals()
	##CandleFetcher.update_all()
	##CandleFetcher.fetch_candles_after_date("BTC", date_to_timestamp("2017-1-1"), 7200)
	##CandleFetcher.fetch_candles_after_date("NXT", date_to_timestamp("2016-1-1"), 7200)
	
	##CandleFetcher.cut_table(table_names.BTC_300, date_to_timestamp("2017-2-17"))
	##CandleFetcher.cut_table(table_names.BTC_300, date_to_timestamp("2017-1-1"), date_to_timestamp("2017-2-1"))
	##CandleFetcher.cut_table(table_names.BTC_300, date_to_timestamp("2017-1-1"), date_to_timestamp("2017-2-1"))
	##CandleFetcher.cut_table(table_names.BTC_300, date_to_timestamp("2017-2-16"), date_to_timestamp("2017-2-17"))


	##strat = ShortTermStrategy(table_names.BTC_300)
	##date2 = date1+ 4*HALF_DAY
	##tn = CandleFetcher.cut_table(table_names.BTC_300, date1, date2)
	##strat = ShortTermStrategy(tn)
	##DBManager.drop_table(tn)
	##total_balance = 0
	##total_percent = 1
	##date1 = date_to_timestamp("2016-6-1") 
	##for i in range(9):
		##date2 = date1+ 60*HALF_DAY
		##tn = CandleFetcher.cut_table(table_names.BTC_300, date1, date2)
		##(balance, percent) = simulate_short_term_strategy([tn])
		##DBManager.drop_table(tn)
		##date1 = date2
		##total_balance += balance
		##total_percent *= (percent+1)
	##print "Total Balance:", total_balance
	##print "Total Percent:", total_percent
	
	##total = 1
	##date1 = date_to_timestamp("2016-6-1")
	##for i in range(18):
		##date2 = date1+ 30*HALF_DAY
		##tn = CandleFetcher.cut_table(table_names.BTC_300, date1, date2)
		##strat = ShortTermStrategy(tn)
		##strat = BollingerStrategy(tn, set_default = True)
		##total *= (1+test_against_normal(strat))
		##DBManager.drop_table(tn)
		##date1 = date2
	##print(total)
	

	##date2 = date1+ HALF_DAY
	##tn = CandleFetcher.cut_table(table_names.BTC_300, date1, date2)
	##simulate_short_term_strategy([tn])
	

	##populate_exp_avg_points(table_name_ETH_14400)
	##grab_trend_all(trend_name_XMR, "XMR")
	##cut_trend(table_name_ETH_14400, table_name_ETH)
	
	##strat = ShortTermStrategy(table_names.BTC_2017_02_19_300)	

	##DBManager.drop_matching_tables("OSCIL")
	##simulate_oscil_strategy(table_names.BIG_HALF1_14400)
	##simulate_bollinger_strategy(table_names.BIG_HALF2_7200)
	##simulate_bollinger_strategy([table_names.NXT_HALF2_7200])
	##simulate_bollinger_strategy(table_names.BIG_HALF2_7200)
	##simulate_bollinger_strategy([table_names.BTC_HALF2_7200])
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
	
	##optimize(table_names.BIG_HALF2_7200)
	
	##simulate_bollinger_strategy([table_names.XRP_HALF, table_names.LTC_HALF, table_names.ETC_HALF, table_names.REP_HALF, table_names.DASH_HALF])
	
	
	
	##present_bollinger(table_names.BTC_7200)
	##present_bollinger(table_names.DASH_14400)

	##simulate(table_name_BTC_14400)
	##simulate(table_name_LTC_14400)

def test_against_normal(strat):
	print("**************************************NORMAL************************************************")
	tn = strat.table_name
	trade_sim = TradeSimulator([tn], [strat], to_print_trades = True, to_log = True)
	trade_sim.run()
	f_bitsec = trade_sim.bit_sec
	f_bits = trade_sim.total_bits_bought_array[0]
	f_balance = trade_sim.balance
	f_profit_percent = trade_sim.profit_percent

	strat = NormalStrategy(tn, f_bits, f_bitsec)
	trade_sim = TradeSimulator([tn], [strat], to_log = True)
	trade_sim.run()
	s_bitsec = trade_sim.bit_sec
	s_bits = trade_sim.total_bits_bought_array[0]
	s_balance = trade_sim.balance
	s_profit_percent = trade_sim.profit_percent
	
	print()
	##print "First: bits, bitsec", f_bits, f_bitsec
	##print "Second: bits, bitsec", s_bits, s_bitsec
	print(("balance dif:", f_balance-s_balance))
	print(("profit dif:", f_profit_percent-s_profit_percent))
	print("**************************************NORMAL DONE*******************************************")
	##total = 0
	##for r in strat.runs:
		##total+=r
	##print total/len(strat.runs)
	return f_profit_percent

## optimize parameters
def optimize(table_name_array):
	po = ParameterOptimizer(table_name_array)
	po.optimize_bollinger()

def simulate_short_term_strategy(candle_table_name_array):
	strat_array = []
	for tn in candle_table_name_array:
		strat = ShortTermStrategy(tn)
		strat_array.append(strat)
	trade_sim = TradeSimulator(candle_table_name_array, strat_array, to_log = True)
	trade_sim.run()
	balance = trade_sim.balance
	percent = trade_sim.profit_percent
	return (balance, percent)


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
	##strat_array[0].print_trade_plans()

def simulate_hold_strategy(candle_table_name_array):
	strat_array = []
	for tn in candle_table_name_array:
		strat = HoldStrategy(tn)
		strat_array.append(strat)
	trade_sim = TradeSimulator(candle_table_name_array, strat_array, to_log = True)
	trade_sim.run()

def present_bollinger(candle_table_name):
	strat = BollingerStrategy(candle_table_name)
	print(candle_table_name)
	print(("# of stddev from mean: ", strat.get_current_bb_score()))

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

