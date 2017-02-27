## places orders to poloniex based on signals

from signal_table import SignalTable
from sig import Sig
from poloniex import Poloniex
from order import Order
from order_table import OrderTable
import time
import threading

class OrderMaker:
	
	##factor represents what relative weight to give to each currency when deciding amount bought
	FACTORS = { 
			"BTC" : 0.5,
			"ETH" : 0.25,
			"LTC" : 0.1,
			"XMR" : 0.1,
			"XRP" : 0.025,
			"DASH" : 0.025
	}
	TINY_AMT = 0.00000001
	
	OVERBID_AMOUNT = 0.00001 ##amount to overbid by
	EXPENSE_FRACTION = 0.2 ## what fraction of USDT to use to buy for this order

	def __init__(self, signals):
		self.signals = signals
		self.usdt_balance = self.poloniex.returnBalances()["USDT"]
		print self.usdt_balance

	##goes through any buy signals and determines how much to spend on each currency
	def attempt_buys(self):
		##total usdt to distribute among the different buy orders
		usdt_to_use = self.EXPENSE_FACTOR* self.usdt_balance
		total_adjusted_sig_amount = 0
		for s in signals:
			if s.type == Sig.BUY:
				total_adjusted_sig_amount += s.amount* self.FACTORS[s.sym]

		for s in signals:
			if s.type == Sig.BUY:
				s_fraction =  (s.amount* self.FACTORS[s.sym])/total_adjusted_sig_amount
				sym_money_to_spend = s_fraction * self.usdt_to_use
				place_buy_order(self, s.sym, sym_money_to_use)

	##ASAP buy sym money worth of currency sym at the lowest ask price
	@staticmethod
	def fast_buy(sym, sym_money):
		curr_pair = "USDT_" + sym
		rate = OrderMaker.get_instant_rate_ask(curr_pair, sym_money)
		amount = sym_money/rate
		print "Fast buying", curr_pair, ":", amount, "at", rate 
		order = OrderMaker.place_buy_order(curr_pair, rate, amount)
	
	##ASAP sell sym money worth of currency sym at the highest bid price
	@staticmethod
	def fast_sell(sym, sym_money):
		curr_pair = "USDT_" + sym
		rate = OrderMaker.get_instant_rate_bid(curr_pair, sym_money)
		amount = sym_money/rate
		print "Fast selling", curr_pair, ":", amount, "at", rate 
		order = OrderMaker.place_sell_order(curr_pair, rate, amount)

	## creates a thread that performs slow buy and runs slow_buy_code	
	@staticmethod
	def slow_buy(sym, sym_money):
		t = threading.Thread(target = OrderMaker.slow_buy_code, args = (sym, sym_money,))
		t.start()
	
	## creates a thread that performs slow sell and runs slow_sell_code	
	@staticmethod
	def slow_sell(sym, sym_money):
		t = threading.Thread(target = OrderMaker.slow_sell_code, args = (sym, sym_money,))
		t.start()
	
	##Buy sym money worth of sym currency by repeatedly posting order at slightly more than current highest
	@staticmethod
	def slow_buy_code(sym, sym_money):
		polo = Poloniex.get_instance()

		##place initial buy order
		curr_pair = "USDT_" + sym
		rate = OrderMaker.get_top_bid(curr_pair) + OrderMaker.TINY_AMT
		amount = sym_money/rate
		print "Slow buying", curr_pair, ":", amount, "at", rate 
		order = OrderMaker.place_buy_order(curr_pair, rate, amount)
		time.sleep(0.2)
		while(order.is_active()):
			top_rate = OrderMaker.get_top_bid(curr_pair)
			
			## if i've been overbid, modify overbid to get to top of list
			if top_rate > order.rate: 
				new_rate = top_rate + OrderMaker.TINY_AMT
				date_placed = time.time()
				move_result = polo.api_query("moveOrder", {'orderNumber': order.id, 'rate' : new_rate})
				new_order_id = move_result['orderNumber']
				if new_order_id != None:
					print "Updating slow buying", curr_pair, ":", amount, "at", new_rate
					order.drop()
					new_order = Order(Order.ORDER_ACTIVE, new_order_id, curr_pair, date_placed, order.amount, new_rate, Order.BID) 
					new_order.save()
					order = new_order
			time.sleep(0.2)
			order.polo_update()
	
	##Sell sym money worth of sym currency by repeatedly posting order at slightly less than current lowest ask
	@staticmethod
	def slow_sell_code(sym, sym_money):
		polo = Poloniex.get_instance()

		##place initial buy order
		curr_pair = "USDT_" + sym
		rate = OrderMaker.get_bottom_ask(curr_pair) - OrderMaker.TINY_AMT
		amount = sym_money/rate
		print "Slow selling", curr_pair, ":", amount, "at", rate 
		order = OrderMaker.place_sell_order(curr_pair, rate, amount)
		time.sleep(0.2)
		while(order.is_active()):
			bottom_rate = OrderMaker.get_bottom_ask(curr_pair)
			
			## if i've been overbid, modify overbid to get to top of list
			if bottom_rate < order.rate: 
				new_rate = bottom_rate - OrderMaker.TINY_AMT
				date_placed = time.time()
				move_result = polo.api_query("moveOrder", {'orderNumber': order.id, 'rate' : new_rate})
				new_order_id = move_result['orderNumber']
				if new_order_id != None:
					print "Updating slow selling", curr_pair, ":", amount, "at", new_rate
					order.drop()
					new_order = Order(Order.ORDER_ACTIVE, new_order_id, curr_pair, date_placed, order.amount, new_rate, Order.ASK) 
					new_order.save()
					order = new_order
			time.sleep(0.2)
			order.polo_update()

	##places a buy order to buy curr_pair at rate and amount given 
	@staticmethod
	def place_buy_order(curr_pair, rate, amount):
		date_placed = time.time()
		order_id = Poloniex.get_instance().buy(curr_pair, rate, amount)["orderNumber"]
		##order_num = Poloniex.get_instance().api_query("buy", {'currencyPair': curr_pair, 'rate' : rate, 'amount' : amount, 'fillOrKill' : 1})
		o = None
		if order_id != None:
			o = Order(Order.ORDER_ACTIVE, order_id, curr_pair, date_placed, amount, rate, Order.BID) 
			o.save()
		return o
	
	##places a sell order to buy curr_pair at rate and amount given 
	@staticmethod
	def place_sell_order(curr_pair, rate, amount):
		date_placed = time.time()
		order_id = Poloniex.get_instance().sell(curr_pair, rate, amount)["orderNumber"]
		o = None
		if order_id != None:
			o = Order(Order.ORDER_ACTIVE, order_id, curr_pair, date_placed, amount, rate, Order.ASK) 
			o.save()
		return o
	
	##update order table
	##possibly move completed active order to filed orders 
	@staticmethod
	def update_orders():
		polo = Poloniex.get_instance()
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
			polo_data = polo.api_query("returnOpenOrders", {'currencyPair': curr_pair})
			
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
		

	##return the rate of the top current bid for the currency pair
	@staticmethod
	def get_top_bid(curr_pair):
		bids =  Poloniex.get_instance().returnOrderBook(curr_pair)["bids"]
		top_bid = bids[0]
		return float(top_bid[0])

	##return the rate of the bottom current ask for the currency pair
	@staticmethod
	def get_bottom_ask(curr_pair):
		asks =  Poloniex.get_instance().returnOrderBook(curr_pair)["asks"]
		bottom_ask = asks[0]
		return float(bottom_ask[0])
	
	##return the rate at which all money is spent to buy instantly at lowest possible price
	@staticmethod
	def get_instant_rate_ask(curr_pair, money):
		asks =  Poloniex.get_instance().returnOrderBook(curr_pair)["asks"]
		i = 0
		for a in asks:
			rate = float(a[0])
			amount = float(a[1]) 
			money_to_spend = rate * amount 
			money -= money_to_spend
			if money < 0:
				return rate
		
	##return the rate at I can instantly sell sym_money worth of curr_pair 
	@staticmethod
	def get_instant_rate_ask(curr_pair, money):
		bids =  Poloniex.get_instance().returnOrderBook(curr_pair)["bids"]
		i = 0
		for a in bids:
			rate = float(a[0])
			amount = float(a[1]) 
			money_to_get = rate * amount 
			money -= money_to_get
			if money < 0:
				return rate
