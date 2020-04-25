import os
import sys
from pathlib import Path
import argparse

PROJECT_DIRECTORY = Path(__file__).parent.absolute()

def addFoldersToPath(directory, recursive=True):
        '''
        Directory has to be pathlib format
        '''
        for item in directory.iterdir():
                if item.is_dir():
                        sys.path.append(str(item))
                        if recursive:
                                addFoldersToPath(item)

addFoldersToPath(PROJECT_DIRECTORY)                             

from candle_fetcher import CandleFetcher
from tools import date_to_timestamp
from poloniex import Poloniex
import table_names
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
from trade_simulator import TradeSimulator
from db_manager import DBManager

HALF_DAY = 43200

def test_strategy(strat_string, start_date, ticker, resolution, num_days):
        total_profit = 1
        total_balance = 0
        total_balance_bitsec = 0
        date1 = date_to_timestamp(start_date)
        for i in range(1):
                date2 = date1+ num_days*2*HALF_DAY
                tn = CandleFetcher.cut_table(eval('table_names.'+ ticker + '_' + resolution), date1, date2)
                strat = eval(strat_string)(tn, calc_stats = False)
                ##strat = BollingerStrategy(tn, set_default = True)
                (profit, balance, balance_bitsec) = test_against_hold(strat)
                total_profit *= 1+profit
                total_balance += balance 
                total_balance_bitsec += balance_bitsec 
                date1 = date2

                ##sc = StatCalculator(tn)
                ##volatility = sc.get_volatility()
                ##volume = sc.get_volume()
                ##print ("Volatility:", volatility)
                ##print ("Volume:", volume)
                DBManager.drop_table(tn)
        print("total profit:", total_profit)
        print("total balance:", total_balance)
        print("total balance bitsec:", total_balance_bitsec)
        ##print(total_profit_bitsec)

def test_against_hold(strat):
	print("**************************************NORMAL************************************************")
	tn = strat.table_name
	trade_sim = TradeSimulator([tn], [strat], limit = -100, to_print_trades = False, to_log = True)
	trade_sim.run()
	f_bitsec = trade_sim.bit_sec
	f_balance = trade_sim.balance
	f_profit_percent = trade_sim.profit_percent
	f_balance_bitsec = trade_sim.profit_per_bitsec

	strat = HoldStrategy(tn, 100)
	trade_sim = TradeSimulator([tn], [strat], limit = -100, to_log = True)
	trade_sim.run()
	s_bitsec = trade_sim.bit_sec
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
	##return f_profit_percent
	return (f_profit_percent, f_balance, f_balance_bitsec)

parser = argparse.ArgumentParser(description='Simulates strategies against historical data to maximize dissapointment in real life')
parser.add_argument('--strategy', help='Name of strategy class i.e ShortTermStrategy', required=True)
parser.add_argument('--ticker', help='Test this tickers data, i.e BTC', required=True)
parser.add_argument('--start_date', help='Test after this date, i.e 2019-6-1', required=True)
parser.add_argument('--resolution', help='Width of each candle in seconds, i.e 300, 7200, 14400', required=True)
parser.add_argument('--num_days', help='Number of days to run simulation for', required=True)
args = parser.parse_args()

test_strategy(args.strategy, args.start_date, args.ticker, args.resolution, int(args.num_days))





