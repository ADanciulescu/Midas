import urllib.request
import urllib.parse
import json
import time
import hmac,hashlib
import requests
import threading

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
	return time.mktime(time.strptime(datestr, format))

class Poloniex:
	
	INSTANCE = None

	def __init__(self):
		with open('./exchange_clients/poloniex_secret.key', 'r') as myfile:
			key = myfile.readline().rstrip()
			secret = myfile.readline().rstrip()
		self.APIKey = key
		self.Secret = secret
		self.lock = threading.Lock()

	
	@classmethod
	def get_instance(cls):
		if cls.INSTANCE is None:
			cls.INSTANCE = cls()
		return cls.INSTANCE

	def post_process(self, before):
		after = before
		# Add timestamps if there isnt one but is a datetime
		if('return' in after):
			if(isinstance(after['return'], list)):
				for x in xrange(0, len(after['return'])):
					if(isinstance(after['return'][x], dict)):
						if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
							after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))

		return after

	def api_query(self, command, req={}):
		self.lock.acquire()
		##print("**********************query********************************")
		
		try:		
			if(command == "returnTicker" or command == "return24Volume"):
				ret = urllib.request.urlopen(urllib.request.Request('https://poloniex.com/public?command=' + command))
				ret_decoded = json.loads(ret.read().decode('utf-8'))
			elif(command == "returnOrderBook"):
				ret = urllib.request.urlopen(urllib.request.Request('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
				ret_decoded = json.loads(ret.read().decode('utf-8'))
			elif(command == "returnMarketTradeHistory"):
				ret = urllib.request.urlopen(urllib.request.Request('https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(req['currencyPair'])))
				ret_decoded = json.loads(ret.read().decode('utf-8'))
			else:
				req['command'] = command
				req['nonce'] = int(time.time()*1000)
				post_data = urllib.parse.urlencode(req)

				sign = hmac.new(self.Secret.encode('utf-8'), post_data.encode('utf-8'), hashlib.sha512).hexdigest()
				headers = {
						'Sign': sign,
						'Key': self.APIKey
						}

				ret = requests.post('https://poloniex.com/tradingApi', data =  req, headers = headers)
				jsonRet = json.loads(ret.text)
				ret_decoded = self.post_process(jsonRet)
		except json.decoder.JSONDecodeError:
			print("***************************************api query ERROR**************************************************")
			ret_decoded = None
			
		time.sleep(0.2)
		self.lock.release()
		return ret_decoded


	def returnTicker(self):
		return self.api_query("returnTicker")

	def return24Volume(self):
		return self.api_query("return24Volume")

	def returnOrderBook (self, currencyPair):
		return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

	def returnMarketTradeHistory (self, currencyPair):
		return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})


	# Returns all of your balances.
	# Outputs: 
	# {"BTC":"0.59098578","LTC":"3.31117268", ... }
	def returnBalances(self):
		return self.api_query('returnBalances')

	# Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
	# Inputs:
	# currencyPair  The currency pair e.g. "BTC_XCP"
	# Outputs: 
	# orderNumber   The order number
	# type          sell or buy
	# rate          Price the order is selling or buying at
	# Amount        Quantity of order
	# total         Total value of order (price * quantity)
	def returnOpenOrders(self,currencyPair):
		return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})


	# Returns your trade history for a given market, specified by the "currencyPair" POST parameter
	# Inputs:
	# currencyPair  The currency pair e.g. "BTC_XCP"
	# Outputs: 
	# date          Date in the form: "2014-02-19 03:44:59"
	# rate          Price the order is selling or buying at
	# amount        Quantity of order
	# total         Total value of order (price * quantity)
	# type          sell or buy
	def returnTradeHistory(self,currencyPair):
		return self.api_query('returnTradeHistory',{"currencyPair":currencyPair})

	# Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
	# Inputs:
	# currencyPair  The curreny pair
	# rate          price the order is buying at
	# amount        Amount of coins to buy
	# Outputs: 
	# orderNumber   The order number
	def buy(self,currencyPair,rate,amount):
		return self.api_query('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

	# Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
	# Inputs:
	# currencyPair  The curreny pair
	# rate          price the order is selling at
	# amount        Amount of coins to sell
	# Outputs: 
	# orderNumber   The order number
	def sell(self,currencyPair,rate,amount):
		return self.api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

	# Cancels an order you have placed in a given market. Required POST parameters are "currencyPair" and "orderNumber".
	# Inputs:
	# currencyPair  The curreny pair
	# orderNumber   The order number to cancel
	# Outputs: 
	# succes        1 or 0
	def cancel(self,currencyPair,orderNumber):
		return self.api_query('cancelOrder',{"currencyPair":currencyPair,"orderNumber":orderNumber})

	# Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."} 
	# Inputs:
	# currency      The currency to withdraw
	# amount        The amount of this coin to withdraw
	# address       The withdrawal address
	# Outputs: 
	# response      Text containing message about the withdrawal
	def withdraw(self, currency, amount, address):
		return self.api_query('withdraw',{"currency":currency, "amount":amount, "address":address})
