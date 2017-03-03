##used to normalize for big trends in a currency
##takes in bits bought and total bitsec by another strategy
##performs random trades that have same bits and bitsec
from operation import Operation
from candle_table import CandleTable
from trade_simulator import TradeSimulator
from random import randint

class NormalStrategy:

	NAME = "NORMAL"
	PBUY = 1 ## probability to buy all at any one time

	def __init__(self, table_name, bits, bitsec):
		self.table_name = table_name
		self.bits = bits
		self.bitsec = bitsec
		
		self.candles = CandleTable.get_candle_array(table_name)
		self.period = float(CandleTable.get_period(table_name))
		self.buy_amt = self.calc_buy_amt()

		self.runs = [0]

	##calculates buy amount
	def calc_buy_amt(self):
		if self.bits > 0:
			self.bitsperiod = self.bitsec/float(self.period)
			##solve (1-PSELL)/PSELL = 2*bitperiod/bits
			self.psell = 1/(1+(2*self.bitsperiod/float(self.bits)))
			##print "Psell:", self.psell
			self.exp_buy_run_len = (1-self.psell)/float(self.psell)
			##print "Run len:", self.exp_buy_run_len
			num_candles = len(self.candles)
			exp_num_runs = num_candles/(self.exp_buy_run_len+1)
			##print "Num Runs", exp_num_runs
			##exp_buys_per_run = self.PBUY*exp_buy_run_len
		
			bitsperiod_per_run = self.bitsperiod/exp_num_runs
			buy_amt = bitsperiod_per_run/(self.exp_buy_run_len*(self.exp_buy_run_len/2)*self.PBUY)
			
			
			self.rand_int_sell = randint(0,int(self.exp_buy_run_len))
			##print "Buy amt:", buy_amt	
			return buy_amt
		else:
			return 0


	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits):
		if self.bits > 0:
			rand_int_buy = randint(1,100)
			if candle_num % int(self.exp_buy_run_len+1) == self.rand_int_sell:
				self.runs.append(0)
				return Operation(Operation.SELL_OP, bits)
			elif rand_int_buy <= (self.PBUY)*100:
				self.runs[-1] += 1
				return Operation(Operation.BUY_OP, self.buy_amt)
			else:
				self.runs[-1] += 1
				return Operation(Operation.NONE_OP, 0)
		else:
			return Operation(Operation.NONE_OP, 0)
			
