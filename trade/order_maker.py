## places orders to poloniex based on signals

from signal_table import SignalTable
from sig import Sig
from poloniex import Poloniex

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
	
	OVERBID_AMOUNT = 0.00001 ##amount to overbid by
	EXPENSE_FRACTION = 0.2 ## what fraction of USDT to use to buy for this order

	def __init__(self, signals):
		self.signals = signals
		self.poloniex = Poloniex()
		self.usdt_balance = self.poloniex.returnBalances()["USDT"]

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



	def place_buy_order(self, sym, sym_money):
		curr_pair = "USDT_" + sym
		rate = self.get_top_buy_reate(curr_pair)
		amount = sym_money/rate
		order_num = self.poloniex.buy(curr_pair, rate, amount)
		if order_num != None:
			pass
			##TODO: START HERE

	def get_top_buy_rate(self, curr_pair):
		bids =  self.poloniex.returnOrderBook(curr_pair)["bids"]
		top_bid = bids[0]
		return top_bid[0]


