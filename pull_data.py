import os
import sys
from pathlib import Path
import argparse

PROJECT_DIRECTORY = Path(__file__).parent.absolute()

from utils import addFoldersToPath

addFoldersToPath(PROJECT_DIRECTORY)
				

from candle_fetcher import CandleFetcher
from tools import date_to_timestamp
from poloniex import Poloniex


parser = argparse.ArgumentParser(description='Pulls so much data, youll get tired of pulling!')
parser.add_argument('--ticker', help='Pull data on this ticker, i.e BTC', required=True)
parser.add_argument('--start_date', help='Pull data after this date, i.e 2019-6-1', required=True)
parser.add_argument('--resolution', help='Width of each candle in seconds, i.e 300, 7200, 14400', required=True)
args = parser.parse_args()

CandleFetcher.fetch_candles_after_date(args.ticker, date_to_timestamp(args.start_date), int(args.resolution))
