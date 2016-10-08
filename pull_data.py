import urllib
import urllib2
import json
import sqlite3
from db_manager import DBManager

def pull_data():
	chart_data_endpoint = "https://poloniex.com/public?command=returnChartData"
	sample = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_XMR&start=1405699200&end=9999999999&period=14400"
	start = 1470628800 ## aug 8 2016
	end = 9999999999 ## present
	period = 14400 ## in seconds
	currency_pair = "USDT_BTC"

	url = chart_data_endpoint + "&" + "currencyPair=" + currency_pair + "&" + "start=" + str(start) + "&" + "end=" + str(end) + "&" + "period=" + str(period)
	print url
	print sample

	response = urllib2.urlopen(url)
	data = json.load(response)
	print data

db_manager = DBManager()
db_manager.create_data_table("eth_test")
##db_manager.drop_table("eth_test1")


