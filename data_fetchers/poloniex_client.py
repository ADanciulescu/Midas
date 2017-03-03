## class hits the poloniex api and loads data into DB

import urllib
import urllib2
import json
import sqlite3
from candle_parser import CandleParser


class PoloniexClient:

	POLO_ENDPOINT = "https://poloniex.com/public"
	CMD_CANDLE = "?command=returnChartData"
	CMD_ORDER_BOOK = "?command=returnOrderBook"

	def __init__(self, table_name):
		self.table_name = table_name

	##gets candle data from endpoint and adds it to db
	##called from main
	def populate_candle_db(self, curr_ref, curr_target, start, end, period):
		curr_pair = curr_ref + "_" + curr_target
		##pull raw json data from endpoint
		data = self.pull_candle_data(curr_pair, start, end, period)
		self.store_candle_data(data)
	
	##enters data into db
	def store_candle_data(self, data):
		tp = CandleParser(self.table_name, data)

	##returns raw json data from candle endpoint	
	def pull_candle_data(self, currency_pair, start, end, period):
		url = PoloniexClient.POLO_ENDPOINT + PoloniexClient.CMD_CANDLE + "&" + "currencyPair=" + currency_pair + "&" + "start=" + str(start) + "&" + "end=" + str(end) + "&" + "period=" + str(period)
		response = urllib2.urlopen(url)
		data = json.load(response)
		return data

