## places orders to poloniex based on signals

from signal_table import SignalTable
from sig import Sig
from poloniex import Poloniex
from order import Order
from order_table import OrderTable
import time
import threading
import calendar

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
	return calendar.timegm(time.strptime(datestr, format))

class OrderMaker:
	
	##factor represents what relative weight to give to each currency when deciding amount bought
	FACTORS = { 
			"BTC" : 0.5,
			"ETH" : 0.25,
			"LTC" : 0.1,
			"XMR" : 0.1,
			"REP" : 0.025,
			"DASH" : 0.025
	}
	
	##amounts of each symbol to trade
	SYM_AMOUNTS = { 
			"BTC" : 175,
			"ETH" : 200,
			"XMR" : 175,
			"DASH" : 150,
			"ETC" : 125,
			"LTC" : 75,
			"REP" : 75,
			"NXT" : 75,
			"ZEC" : 150
	}

	SYMS = ["BTC", "ETH", "XMR", "DASH", "REP", "NXT", "ETC", "LTC", "ZEC"]

	TINY_AMT = 0.00000001
	
	OVERBID_AMOUNT = 0.00001 ##amount to overbid by
	EXPENSE_FRACTION = 0.2 ## what fraction of USDT to use to buy for this order

	def __init__(self):
		self.polo = Poloniex.get_instance()
		self.is_owned = {}
		self.on_order_balances = {}
		self.available_balances = {}
		self.total_balances = {}
		
		for s in self.SYMS:
			self.on_order_balances[s] = 0
			self.available_balances[s] = 0
			self.total_balances[s] = 0
			self.is_owned[s] = False
		
		self.update_balances()

	def update_balances(self):
		info = self.polo.api_query("returnCompleteBalances",{})
		if info is None:
			print("API error unable to update_balances")
		else:
			for s in self.SYMS:
				available_amt = float(info[s]['available'])
				on_order_amt = float(info[s]['onOrders'])
				self.available_balances[s] = available_amt
				self.on_order_balances[s] = on_order_amt
				self.total_balances[s] = available_amt + on_order_amt
				if self.total_balances[s] > 0:
					self.is_owned[s] = True
				else:
					self.is_owned[s] = False 
				


	def get_open_orders(self, curr_pair):
		ret_orders = []
		polo_order_data = self.polo.api_query("returnOpenOrders", {'currencyPair': curr_pair})
		if polo_order_data is None:
			print("API error unable to get_open_orders")
		else:
			for o_data in polo_order_data:
				o = Order(Order.ORDER_ACTIVE, o_data['orderNumber'], curr_pair, 0, o_data['amount'], o_data['rate'], o_data['type']) 
				ret_orders.append(o)

		return ret_orders

	
	## slow buy when signal says to buy, slow sell when signal says to sell
	def handle_signal_classic(self, signal):
		amt = self.SYM_AMOUNTS[signal.sym]
		curr_pair = "USDT_" + signal.sym
		
		open_orders = []
		if self.on_order_balances[signal.sym] > 0:
			open_orders = self.get_open_orders(curr_pair)

		if len(open_orders) > 1:
			print ("More than 1 order on:". curr_pair)

		if signal.type == "BUY":
			if len(open_orders) > 0: ##if open orders exist already for this curr_pair
				if open_orders[0].type == Order.BID: ##if buy already exists do nothing
					pass
				else: ##if sell order already exists cancel it and buy amt_desired - amt_held
					cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': open_orders[0].id})
					if cancel_result is None:
						print("API error unable to cancel order")
					amt_held_in_sym = open_orders[0].amount
					amt_held_in_usd = amt_held_in_sym/signal.price
					self.slow_buy(signal.sym, amt - amt_held_in_usd, limit = (signal.price*1.005))
			else:
				self.slow_buy(signal.sym, amt, limit = (signal.price*1.005))

		elif signal.type == "SELL":
			if len(open_orders) > 0: ##if open orders exist already for this curr_pair
				if open_orders[0].type == Order.BID: ##if buy already cancel it and sell all 
					cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': open_orders[0].id})
					if cancel_result is None:
						print("API error unable to cancel order")
					self.slow_sell(signal.sym, amt, sell_all = True, limit = (signal.price*0.995))
				else: ##if sell order already exists do nothing
					pass
			else:
				self.slow_sell(signal.sym, amt, sell_all = True, limit = (signal.price*0.995))

	## instead of signals triggering buy/sell, orders are preplaced based on operating range
	def handle_signal_preorder(self, signal, operating_range):
		sym = signal.sym
		max_usd_amt = self.SYM_AMOUNTS[sym]
		owned_amt = self.curr_available_balances[sym]
		curr_pair = "USDT_" + sym
		polo_order_data = self.polo.api_query("returnOpenOrders", {'currencyPair': curr_pair})

		if len(polo_order_data) > 2:
			print("something is wrong more than 2 open orders for a specific currency")

		##for s in self.SYMS:
			##print(s, self.curr_available_balances[s])

		##get information about currently existing open buy/sell orders
		existing_buy_order = None
		existing_sell_order = None
		for o in polo_order_data:
			if o['type'] == "sell":
				existing_sell_order = Order(Order.ORDER_ACTIVE, o['orderNumber'], curr_pair, 0, o['amount'], o['rate'], Order.ASK) 
			elif o['type'] == "buy":
				existing_buy_order = Order(Order.ORDER_ACTIVE, o['orderNumber'], curr_pair, 0, o['amount'], o['rate'], Order.BID) 
		
		buy_usd_amt = max_usd_amt - owned_amt*signal.price

		floor = operating_range[0]
		ceiling = operating_range[1]
		
		sym_amt = owned_amt 
		if existing_sell_order is not None:
			if ceiling == -1:
				print("Cancelling sell order", curr_pair)
				cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': existing_sell_order.id})
			else:
				print(("Updating preselling", curr_pair, ":", existing_sell_order.amount, "at", ceiling))
				move_result = self.polo.api_query("moveOrder", {'orderNumber': existing_sell_order.id, 'rate' : ceiling, 'amount' : sym_amt})
		else:
			if ceiling == -1:
				return
			else:
				if sym_amt > 0:
					print(("Creating presell", curr_pair, ":", sym_amt, "at", ceiling))
					self.place_sell_order(curr_pair, ceiling, sym_amt)
		
		if floor != -1:
			sym_amt = buy_usd_amt/floor
		else:
			sym_amount = -1
		if existing_buy_order is not None:
			if floor == -1 or sym_amt <= 0:
				print("Cancelling buy order", curr_pair)
				cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': existing_buy_order.id})
			else:
				print(("Updating prebuying", curr_pair, ":", existing_buy_order.amount, "at", floor))
				move_result = self.polo.api_query("moveOrder", {'orderNumber': existing_buy_order.id, 'rate' : sym_amt})
		else:
			if floor == -1:
				return
			else:
				if sym_amt > 0:
					print(("Creating prebuy", curr_pair, ":", sym_amt, "at", floor))
					self.place_buy_order(curr_pair, floor, sym_amt)
			

	##ASAP buy sym money worth of currency sym at the lowest ask price
	def fast_buy(self, sym, sym_money):
		curr_pair = "USDT_" + sym
		rate = self.get_instant_rate_ask(curr_pair, sym_money)
		amount = sym_money/rate
		print(("Fast buying", curr_pair, ":", amount, "at", rate))
		order = self.place_buy_order(curr_pair, rate, amount)
	
	##ASAP sell sym money worth of currency sym at the highest bid price
	def fast_sell(self, sym, sym_money):
		curr_pair = "USDT_" + sym
		rate = self.get_instant_rate_bid(curr_pair, sym_money)
		amount = sym_money/rate
		print(("Fast selling", curr_pair, ":", amount, "at", rate))
		order = self.place_sell_order(curr_pair, rate, amount)

	## creates a thread that performs slow buy and runs slow_buy_code	
	def slow_buy(self, sym, sym_money, limit =  100000):
		t = threading.Thread(target = self.slow_buy_code, args = (sym, sym_money, limit))
		t.start()
	
	## creates a thread that performs slow sell and runs slow_sell_code	
	def slow_sell(self, sym, sym_money, limit = 0, sell_all = False):
		t = threading.Thread(target = self.slow_sell_code, args = (sym, sym_money, limit, sell_all))
		t.start()
	
	##Buy sym money worth of sym currency by repeatedly posting order at slightly more than current highest bid
	def slow_buy_code(self, sym, sym_money, limit):
		

		##place initial buy order
		curr_pair = "USDT_" + sym
		rate = self.get_top_bid(curr_pair) + OrderMaker.TINY_AMT

		amount = sym_money/rate

		initial_amount = amount
		
		
		print(("Slow buying", curr_pair, ":", amount, "at", rate))
		order = self.place_buy_order(curr_pair, rate, amount)
		
		while(order.is_active()):
			new_rate = self.get_top_bid(curr_pair, order)
			amount_filled = initial_amount - order.amount
			
			## if i've been overbid, modify my bid to get to top of list
			if new_rate != order.rate:

				if new_rate > limit: ##if surpassed limit cancel order
					cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': order.id})
					if cancel_result is None:
						print("API error unable to cancel order")
					else:
						print("order cancelled")
						order.move(Order.ORDER_CANCELLED, amount_filled)
				else:
					move_result = self.polo.api_query("moveOrder", {'orderNumber': order.id, 'rate' : new_rate})
					if move_result is None:
						print("API error unable to move order")
					else:
						if move_result["success"] == 1:
							print(("Updating slow buying", curr_pair, ":", order.amount, "at", new_rate))
							date_placed = time.time()
							new_order_id = move_result['orderNumber']
							order.move(Order.ORDER_FILLED, amount_filled)
							new_order = Order(Order.ORDER_ACTIVE, new_order_id, curr_pair, date_placed, order.amount, new_rate, Order.ASK) 
							new_order.save()
							order = new_order
							initial_amount = order.amount
						else:
							print("Failed to move buy order:", curr_pair, "to new rate:", new_rate)
			order.polo_update()
		print("Done slow BUYING", curr_pair)
	
	
	##Sell sym money worth of sym currency by repeatedly posting order at slightly less than current lowest ask
	def slow_sell_code(self, sym, sym_money, limit, sell_all):
		

		##place initial buy order
		curr_pair = "USDT_" + sym
		rate = self.get_bottom_ask(curr_pair)

		if sell_all:
			self.update_balances()
			amount = self.available_balances[sym]
			if amount == 0:
				return
		else:
			amount = sym_money/rate

		initial_amount = amount
		
		
		print(("Slow selling", curr_pair, ":", amount, "at", rate))
		order = self.place_sell_order(curr_pair, rate, amount)
		
		while(order.is_active()):
			new_rate = self.get_bottom_ask(curr_pair, order)
			amount_filled = initial_amount - order.amount
			
			## if i've been overbid, modify my bid to get to top of list
			if new_rate != order.rate:
				if new_rate < limit: ##if surpassed limit cancel order
					cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': order.id})
					if cancel_result is None:
						print("API error unable to cancel order")
					else:
						print("order cancelled")
						order.move(Order.ORDER_CANCELLED, amount_filled)
				else:
					move_result = self.polo.api_query("moveOrder", {'orderNumber': order.id, 'rate' : new_rate})
					if move_result is None:
						print("API error unable to cancel order")
					else:
						if move_result["success"] == 1:
							print(("Updating slow selling", curr_pair, ":", order.amount, "at", new_rate))
							new_order_id = move_result['orderNumber']
							date_placed = time.time()
							order.move(Order.ORDER_FILLED, amount_filled)
							new_order = Order(Order.ORDER_ACTIVE, new_order_id, curr_pair, date_placed, order.amount, new_rate, Order.ASK) 
							new_order.save()
							order = new_order
							initial_amount = order.amount
						else:
							print("Failed to move sell order:", curr_pair, "to new rate:", new_rate)
			order.polo_update()
		print("Done slow SELLING", curr_pair)

	##places a buy order to buy curr_pair at rate and amount given 
	def place_buy_order(self, curr_pair, rate, amount):
		date_placed = time.time()
		order_result = self.polo.api_query("buy", {"currencyPair" : curr_pair, "rate" : rate, "amount" : amount})
		if order_result is None:
			print("API error unable to place buy order")
			return self.place_buy_order(curr_pair, rate, amount)
		else:
			order_id = order_result["orderNumber"]
			o = None
			o = Order(Order.ORDER_ACTIVE, order_id, curr_pair, date_placed, amount, rate, Order.BID) 
			o.save()
			return o
	
	##places a sell order to buy curr_pair at rate and amount given 
	def place_sell_order(self, curr_pair, rate, amount):
		date_placed = time.time()
		order_result = self.polo.api_query("sell", {"currencyPair" : curr_pair, "rate" : rate, "amount" : amount})
		if order_result is None:
			print("API error unable to place sell order")
			return self.place_sell_order(curr_pair, rate, amount)
		else:
			order_id = order_result['orderNumber']
			o = Order(Order.ORDER_ACTIVE, order_id, curr_pair, date_placed, amount, rate, Order.ASK) 
			o.save()
			return o
	
	##update order table
	##possibly move completed active order to filed orders 
	##TODO: delete or find use, currently not used
	def update_orders(self):
		order_array = OrderTable.get_order_array(Order.ORDER_ACTIVE)
		
		##create a dictionary that groups all orders by key = curr_pair
		order_dict = {}
		for o in order_array:
			if order_dict.get(o.curr_pair) != None:
				order_dict[o.curr_pair].append(o)
			else:
				order_dict[o.curr_pair] = [o]

		for curr_pair in order_dict:
			##get all db orders for the curr_pair
			orders = order_dict[curr_pair]
			##get open polo orders for same pair
			polo_data = self.polo.api_query("returnOpenOrders", {'currencyPair': curr_pair})
			
			##if found db active order on polo, update its info
			##if not means db order is no longer active and should be moved to filled orders db
			for o in orders:
				found = False
				for d in polo_data:
					if o.id == d["orderNumber"]:
						found = True
						o.amount = d["amount"]
						o.update()

				if not found:
					o.drop()
					o.table_name = OrderTable.ORDER_FILLED
					o.date_filled = time.time()
					o.save()
		

	##return the rate of the top current bid for the currency pair(ignores my order)
	def get_top_bid(self, curr_pair, prev_order = None):
		bids_result =  Poloniex.get_instance().returnOrderBook(curr_pair)["bids"]
		if bids_result is None:
			print("API query error unable to get top bid")
			return self.get_top_bid(curr_pair, prev_order)
		else:
			if prev_order == None:
				return float(bids_result[0][0]) + OrderMaker.TINY_AMT
			else:
				if float(bids_result[0][0]) == prev_order.rate: ##if prevorder is already top bid
					return float(bids_result[1][0]) + OrderMaker.TINY_AMT
				else:
					bits_above_my_order = 0
					i=0
					while(float(bids_result[i][0]) > prev_order.rate):
						bits_above_my_order += float(bids_result[i][1])
						i += 1

					##if there is a substantial amount of bits priced over my prev_order, return top bid
					##else return prev order rate
					if bits_above_my_order > prev_order.amount*0.25:
						return float(bids_result[0][0]) + OrderMaker.TINY_AMT
					else:
						return prev_order.rate
	
	##return the rate of the current bottom ask for the currency pair(ignores my order)
	def get_bottom_ask(self, curr_pair, prev_order = None):
		asks_result =  Poloniex.get_instance().returnOrderBook(curr_pair)["asks"]
		if asks_result is None:
			print("API query error unable to get bottom ask")
			return self.get_bottom_ask(curr_pair, prev_order)
		else:
			if prev_order == None:
				return float(asks_result[0][0]) - OrderMaker.TINY_AMT
			else:
				if float(asks_result[0][0]) == prev_order.rate: ##if prevorder is already bottom ask 
					return float(asks_result[1][0]) - OrderMaker.TINY_AMT
				else:
					bits_below_my_order = 0
					i=0
					while(float(asks_result[i][0]) < prev_order.rate):
						##print asks[i][0], "at", asks[i][1]
						bits_below_my_order += float(asks_result[i][1])
						i += 1

					##if there is a substantial amount of bits priced under my prev_order, return bottom ask
					##else return prev order rate
					if bits_below_my_order > prev_order.amount*0.25:
						return float(asks_result[0][0]) - OrderMaker.TINY_AMT
					else:
						return prev_order.rate

	##return the rate at which all money is spent to buy instantly at lowest possible price
	def get_instant_rate_bid(self, curr_pair, money):
		asks_result =  Poloniex.get_instance().returnOrderBook(curr_pair)["asks"]
		if asks_result is None:
			print("API query error unable to get instant bid")
			return self.get_instant_rate_bid(curr_pair, money)
		else:
			i = 0
			for a in asks_result:
				rate = float(a[0])
				amount = float(a[1]) 
				money_to_spend = rate * amount 
				money -= money_to_spend
				if money < 0:
					return rate
		
	##return the rate at I can instantly sell sym_money worth of curr_pair 
	def get_instant_rate_ask(self, curr_pair, money):
		bids_result =  Poloniex.get_instance().returnOrderBook(curr_pair)["bids"]
		if bids_result is None:
			print("API query error unable to get instant ask")
			return self.get_instant_rate_ask(curr_pair, money)
		else:
			i = 0
			for a in bids_result:
				rate = float(a[0])
				amount = float(a[1]) 
				money_to_get = rate * amount 
				money -= money_to_get
				if money < 0:
					return rate

	##returns (bottoms_ask, top_bid) for given currency pair
	@staticmethod
	def get_spread(curr_pair):
		orders_result =  Poloniex.get_instance().returnOrderBook(curr_pair)
		if orders_result is None:
			print("API query error unable to get spread")
			return self.get_spread(curr_pair)
		else:
			bids =  orders_result["bids"]
			asks =  orders_result["asks"]
			return(float(bids[0][0]), float(asks[0][0]))
	
	##returns last trade rate for given currency pair before the given date
	@staticmethod
	def get_last_trade_rate(curr_pair, date):
		trades_result =  Poloniex.get_instance().returnMarketTradeHistory(curr_pair)
		if trades_result is None:
			print("API query error unable to get trades")
			return self.get_last_trade_rate(curr_pair, date)
		else:
			for i in range(len(trades_result)):
				##print(t)	
				if createTimeStamp(trades_result[i]['date']) < date:
					rate = float(trades_result[i]['rate'])
					return rate
