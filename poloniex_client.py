## class hits the poloniex api and loads data into DB

import urllib
import urllib2
import json
import sqlite3
from db_manager import DBManager
from tick_parser import TickParser


class PoloniexClient:

	POLO_ENDPOINT = "https://poloniex.com/public"
	CMD_CANDLE = "?command=returnChartData"
	CMD_ORDER_BOOK = "?command=returnOrderBook"

	def __init__(self, table_name, start, end, period, currency_pair):
		self.table_name = table_name
		self.start = start
		self.end = end
		self.period = period
		self.currency_pair = currency_pair

	##gets candle data from endpoint and adds it to db
	##called from main
	def run(self):
		##pull raw json data from endpoint
		data = self.pull_candle_data()
		self.store_candle_data(data)
	
	##enters data into db
	def store_candle_data(self, data):
		tp = TickParser(self.table_name, data)

	##returns raw json data from endpoint	
	def pull_candle_data(self):
		url = PoloniexClient.POLO_ENDPOINT + PoloniexClient.CMD_CANDLE + "&" + "currencyPair=" + self.currency_pair + "&" + "start=" + str(self.start) + "&" + "end=" + str(self.end) + "&" + "period=" + str(self.period)
		response = urllib2.urlopen(url)
		data = json.load(response)
		return data

