## places orders to poloniex based on signals

from signal_table import SignalTable
from sig import Sig
from poloniex import Poloniex
from order import Order
from order_table import OrderTable
from order_updater import OrderUpdater
from task import Task
import time
import threading
import calendar

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
	return calendar.timegm(time.strptime(datestr, format))

class OrderMaker:
	
	CURR_PAIR_AMOUNTS = { 
			"USDT_BTC" : 175,
			"USDT_ETH" : 200,
			"USDT_XMR" : 175,
			"USDT_DASH" : 150,
			"USDT_ETC" : 125,
			"USDT_LTC" : 75,
			"USDT_REP" : 75,
			"USDT_NXT" : 75,
			"USDT_ZEC" : 150,
			"USDT_XRP" : 0
	}
	
	TINY_AMT = 0.00000001
	FAIL = "FAIL"
	SUCCESS = "SUCCESS"

	def __init__(self, order_updater, scheduler):
		self.polo = Poloniex.get_instance()
		self.order_updater = order_updater
		self.scheduler = scheduler
		
	
	## slow buy when signal says to buy, slow sell when signal says to sell
	def handle_signal_classic(self, signal):
		curr_pair = "USDT_" + signal.sym
		amt_in_usd = self.CURR_PAIR_AMOUNTS[curr_pair]
		

		sym_info = self.order_updater.sym_infos[signal.sym]
		open_buy_orders = sym_info.open_buy_orders
		open_sell_orders = sym_info.open_sell_orders

		if signal.type == "BUY":
			if len(open_buy_orders) > 0: ##if open buy orders exist already for this curr_pair do nothing
				return
			if len(open_sell_orders) > 0: ##if open sell orders exist already for this curr_pair cancel them then slow buy
				self.try_repeatedly(self.cancel_order, sym_info.open_sell_orders[0])
			balance_available = sym_info.available_balance
			balance_in_usd = balance_available * signal.price
			self.slow_buy(signal.sym, amt_in_usd - balance_in_usd, limit = (signal.price*1.005))
		
		elif signal.type == "SELL":
			if len(open_sell_orders) > 0: ##if open sell orders exist already for this curr_pair do nothing
				return
			if len(open_buy_orders) > 0: ##if open buy orders exist already for this curr_pair cancel them then sell
				self.try_repeatedly(self.cancel_order, sym_info.open_buy_orders[0])
			self.slow_sell(signal.sym, 1, sell_all = True, limit = (signal.price*0.995))

	##wrapper for cancel or move order
	##tries repeatedly until either successful or order is confirmed to be already gone
	def try_repeatedly(self, func, order):
		sym = order.get_sym()
		sym_info = self.order_updater.sym_infos[sym]
		open_orders = []
		if order.type == Order.BID:
			open_orders = sym_info.open_buy_orders
		elif order.type == Order.ASK:
			open_orders = sym_info.open_sell_orders

		##if error while cancelling or moving order
		##2 possibilities: 
		##api error -> try again until works, OR
		##order is already gone -> try again until order is gone from sym_info(which updates itself on its own thread)
		while(len(open_orders) > 0):
			result = func(order)
			if result == self.FAIL:
				time.sleep(1)
				if order.type == Order.BID:
					open_orders = sym_info.open_buy_orders
				elif order.type == Order.ASK:
					open_orders = sym_info.open_sell_orders
			elif result == self.SUCCESS:
				return



	def cancel_order(self, order):
		cancel_result = self.polo.api_query("cancelOrder", {'orderNumber': order.id})
		if cancel_result is None:
			print("API error unable to cancel order")
			return self.FAIL
		else:
			print("Successfully cancelled order", order.curr_pair)
			order.drop()
			sym = order.get_sym()
			sym_info = self.order_updater.sym_infos[sym]
			new_balances = self.order_updater.get_available_balances() 
			if order.type == Order.BID:
				sym_info.update(new_balances[sym], [], sym_info.open_sell_orders)
			elif order.type == Order.ASK:
				sym_info.update(new_balances[sym], sym_info.open_buy_orders, [])
			return self.SUCCESS

	def move_order(self, order):
		move_result = self.polo.api_query("moveOrder", {'orderNumber': order.id, 'rate' : order.rate})
		if move_result is None:
			print("API error unable to move order")
			return self.FAIL
		else:
			if move_result["success"] == 1:
				date_placed = time.time()
				new_order_id = move_result['orderNumber']
				new_order = Order(Order.ORDER_ACTIVE, new_order_id, order.curr_pair, date_placed, order.amount, order.rate, order.type) 
				new_order.save()

				sym = order.get_sym()
				sym_info = self.order_updater.sym_infos[sym]
				if order.type == Order.BID:
					sym_info.update(sym_info.available_balance, [new_order], sym_info.open_sell_orders)
				elif order.type == Order.ASK:
					sym_info.update(sym_info.available_balance, sym_info.open_buy_orders, [new_order])
				return self.SUCCESS
			else:
				print("Failed to move buy order:", order.curr_pair, "to new rate:", order.rate)
				return self.FAIL


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

		balance = self.order_updater.sym_infos["USDT"].available_balance

		if sym_money > balance:
			print("Can't buy, not enough funds")
			return
		else:
			##place initial buy order
			curr_pair = "USDT_" + sym
			rate = self.get_top_bid(curr_pair) + OrderMaker.TINY_AMT
			amount = sym_money/rate
			print(("Slow buying", curr_pair, ":", amount, "at", rate))
			order = self.place_buy_order(curr_pair, rate, amount)

			##set up a task to update order
			slow_buy_task = Task(self.slow_buy_update, 0, args = (sym, sym_money, limit))
			self.scheduler.schedule_task(slow_buy_task)

	## creates a thread that performs slow sell and runs slow_sell_code	
	def slow_sell(self, sym, sym_money, limit = 0, sell_all = False):
		##place initial sell order
		curr_pair = "USDT_" + sym
		rate = self.get_bottom_ask(curr_pair)
		if sell_all:
			amount = self.order_updater.sym_infos[sym].available_balance
			if amount == 0:
				return
		else:
			amount = sym_money/rate
		print(("Slow selling", curr_pair, ":", amount, "at", rate))
		order = self.place_sell_order(curr_pair, rate, amount)
		
		
		##set up a task to update order
		slow_sell_task = Task(self.slow_sell_update, 0, args = (sym, sym_money, limit, sell_all))
		self.scheduler.schedule_task(slow_sell_task)
		##t = threading.Thread(target = self.slow_sell_code, args = (sym, sym_money, limit, sell_all))
		##t.start()
	
	##Buy sym money worth of sym currency by repeatedly posting order at slightly more than current highest bid
	def slow_buy_update(self, sym, sym_money, limit):
		curr_pair = "USDT_" + sym
		sym_info = self.order_updater.sym_infos[sym]
		open_buy_orders = sym_info.open_buy_orders
		
		if len(open_buy_orders) == 0:
			print("Done slow BUYING", curr_pair)
			return Task.DONE
		else:
			order = open_buy_orders[0]
			new_rate = self.get_top_bid(curr_pair, order)
			##amount_filled = initial_amount - order.amount
			
			## if i've been overbid, modify my bid to get to top of list
			if new_rate != order.rate:
				if new_rate > limit: ##if surpassed limit cancel order
					self.cancel_order(order)
				else:
					order.rate = new_rate
					print(("Updating slow buying", curr_pair, ":", order.amount, "at", new_rate))
					self.move_order(order)
			return Task.CONTINUE
	
	##Sell sym money worth of sym currency by repeatedly posting order at slightly less than current lowest ask
	def slow_sell_update(self, sym, sym_money, limit, sell_all):
		curr_pair = "USDT_" + sym
		sym_info = self.order_updater.sym_infos[sym]
		open_sell_orders = sym_info.open_sell_orders
	
		if len(open_sell_orders) == 0:
			print("Done slow SELLING", curr_pair)
			return Task.DONE
		else:
			order = open_sell_orders[0]
			new_rate = self.get_bottom_ask(curr_pair, order)
			
			## if i've been underask, modify my ask to get to top of list
			if new_rate != order.rate:
				if new_rate < limit: ##if surpassed limit cancel order
					self.cancel_order(order)
				else:
					order.rate = new_rate
					print(("Updating slow selling", curr_pair, ":", order.amount, "at", new_rate))
					self.move_order(order)
			return Task.CONTINUE
	

	##places a buy order to buy curr_pair at rate and amount given 
	def place_buy_order(self, curr_pair, rate, amount):
		date_placed = time.time()
		order_result = self.polo.api_query("buy", {"currencyPair" : curr_pair, "rate" : rate, "amount" : amount})
		if order_result is None:
			print("API error unable to place buy order")
			return self.place_buy_order(curr_pair, rate, amount)
		else:
			order_id = order_result["orderNumber"]
			o = Order(Order.ORDER_ACTIVE, order_id, curr_pair, date_placed, amount, rate, Order.BID) 
			o.save()

			sym_info = self.order_updater.sym_infos[o.get_sym()]
			sym_info.update(sym_info.available_balance, [o], sym_info.open_sell_orders)
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
			
			sym_info = self.order_updater.sym_infos[o.get_sym()]
			sym_info.update(sym_info.available_balance, sym_info.open_buy_orders, [o])
			return o
	
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
					while(float(bids_result[i][0]) > prev_order.rate) and (bits_above_my_order < prev_order.amount*0.25):
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
					while(float(asks_result[i][0]) < prev_order.rate) and (bits_below_my_order < prev_order.amount*0.25):
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
	
	'''
	## instead of signals triggering buy/sell, orders are preplaced based on operating range
	def handle_signal_preorder(self, signal, operating_range):
		sym = signal.sym
		max_usd_amt = self.SYM_AMOUNTS[sym]
		owned_amt = self.curr_available_balances[sym]
		curr_pair = "USDT_" + sym
		polo_order_data = self.polo.api_query("returnOpenOrders", {'currencyPair': curr_pair})

		if len(polo_order_data) > 2:
			print("something is wrong more than 2 open orders for a specific currency")

		for s in self.SYMS:
			print(s, self.curr_available_balances[s])

		get information about currently existing open buy/sell orders
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
		'''
