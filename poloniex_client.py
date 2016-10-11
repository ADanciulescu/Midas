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

	def __init__(self, table_name):
		self.table_name = table_name

	##gets tick data from endpoint and adds it to db
	##called from main
	def populate_tick_db(self, start, end, period, currency_pair):
		##pull raw json data from endpoint
		data = self.pull_tick_data(start, end, period, currency_pair)
		self.store_tick_data(data)
	
	##enters data into db
	def store_tick_data(self, data):
		tp = TickParser(self.table_name, data)

	##returns raw json data from tick endpoint	
	def pull_tick_data(self, start, end, period, currency_pair):
		url = PoloniexClient.POLO_ENDPOINT + PoloniexClient.CMD_CANDLE + "&" + "currencyPair=" + currency_pair + "&" + "start=" + str(start) + "&" + "end=" + str(end) + "&" + "period=" + str(period)
		response = urllib2.urlopen(url)
		data = json.load(response)
		return data

