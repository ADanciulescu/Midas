## updates open orders
## uses a thread to update every 5 seconds
## order maker uses this as a source of truth about orders

import threading
import time
from order import Order
from order_table import OrderTable
from poloniex import Poloniex
from sym_info import SymInfo

class OrderUpdater:
	##amounts of each symbol to trade

	CURR_PAIRS = ["USDT", "USDT_BTC", "USDT_ETH", "USDT_XMR", "USDT_DASH", "USDT_REP", "USDT_NXT", "USDT_ETC", "USDT_LTC", "USDT_ZEC", "USDT_XRP"]
	
	SYMS = ["USDT", "BTC", "ETH", "XMR", "DASH", "REP", "NXT", "ETC", "LTC", "ZEC", "XRP"]

	RUN_PERIOD = 5 ##update orders and balances every RUN_PERIOD seconds

	def __init__(self):
		self.sym_infos = {}
		self.polo = Poloniex.get_instance()
		for s in self.SYMS:
			si = SymInfo(s)
			self.sym_infos[s] = si


	def run(self):
		t = threading.Thread(target = self.update_orders, args = ())
		t.start()
		
	
	## thread runs this code
	## updates balance and open orders for each sym every RUN_PERIOD
	def update_orders(self):
		last_time = 0 
		while(True):
			print("updating")
			if (time.time() - last_time) > self.RUN_PERIOD:
				available_balances = self.get_available_balances()
				(open_buy_orders, open_sell_orders) = self.get_open_orders()
				
				for s in self.SYMS:
					self.sym_infos[s].update(available_balances[s], open_buy_orders[s], open_sell_orders[s])
				
				last_time = time.time() 
			else:
				time.sleep(1)



	## returns dictionary of open_sell_orders and open_buy_orders for given sym
	def get_open_orders(self):
		open_buy_orders = {}
		open_sell_orders = {}
		polo_order_data = self.polo.api_query("returnOpenOrders", {'currencyPair': "all"})
		if polo_order_data is None:
			print("API error unable to get_open_orders")
			return self.get_open_orders()
		else:
			for s in self.SYMS:
				open_buy_orders[s] = []
				open_sell_orders[s] = []
				curr_pair = "USDT_" + s
				if curr_pair in polo_order_data:
					curr_data = polo_order_data[curr_pair]
					for o_data in curr_data:
						##o = OrderTable.find_order(Order.ORDER_ACTIVE, o_data['orderNumber'])
						o = Order(Order.ORDER_ACTIVE, o_data['orderNumber'], curr_pair, 0, float(o_data['amount']), float(o_data['rate']), o_data['type']) 
						##o.amount = o_data['amount']
						##o.rate = o_data['rate']
						##o.update()
						if o.type == Order.BID:
							open_buy_orders[s].append(o)
						elif o.type == Order.ASK:
							open_sell_orders[s].append(o)

		return (open_buy_orders, open_sell_orders)


	## returns dictionary of balances for each sym
	def get_available_balances(self):
		balances = {}
		info = self.polo.api_query("returnCompleteBalances",{})
		if info is None:
			print("API error unable to update_balances")
			return self.get_available_balances()
		else:
			for s in self.SYMS:
				available_amt = float(info[s]['available'])
				##on_order_amt = float(info[s]['onOrders'])
				balances[s] = available_amt
			return balances
