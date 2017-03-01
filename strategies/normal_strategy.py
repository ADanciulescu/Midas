##used to normalize for big trends in a currency
##takes in bits bought and total bitsec by another strategy
##performs random trades that have same bits and bitsec
from operation import Operation
from candle_table import CandleTable
from trade_simulator import TradeSimulator
from random import randint

class NormalStrategy:

	NAME = "NORMAL"
	PBUY = 0.2 ## probability to sell all at any one time
	NUM_TRADES = 50 ## how many trades to aim for

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
		self.bitsperiod = self.bitsec/self.period
		##solve (1-PSELL)/PSELL = 2*bitperiod/bits
		self.psell = 1/(1+2*self.bitsperiod/float(self.bits))
		##print "Psell:", self.psell
		num_candles = len(self.candles)
		self.exp_buy_run_len = (1-self.psell)/float(self.psell)
		##print "Run len:", self.exp_buy_run_len
		exp_num_runs = num_candles/(self.exp_buy_run_len+1)
		##print "Num Runs", exp_num_runs
		##exp_buys_per_run = self.PBUY*exp_buy_run_len
	
		bitsperiod_per_run = self.bitsperiod/exp_num_runs
		buy_amt = bitsperiod_per_run/(self.exp_buy_run_len*(self.exp_buy_run_len/2)*self.PBUY)
		##print "Buy amt:", buy_amt	
		return buy_amt


	##simply returns name
	def get_name(self):
		return  self.NAME

	##returns market operation
	def decide(self, candle_num, bits):
		##rand_int = randint(1,100)
		##if rand_int <= self.PSELL*100:
			##self.runs.append(0)
			##return Operation(Operation.SELL_OP, bits)
		##elif rand_int <= (self.PSELL+self.PBUY)*100:
			##self.runs[-1] += 1
			##return Operation(Operation.BUY_OP, self.buy_amt)
		##else:
			##self.runs[-1] += 1
			##return Operation(Operation.NONE_OP, 0)
		rand_int_sell = randint(0,self.exp_buy_run_len)
		rand_int_buy = randint(1,100)
		if candle_num % int(self.exp_buy_run_len+1) == rand_int_sell:
			self.runs.append(0)
			return Operation(Operation.SELL_OP, bits)
		elif rand_int_buy <= (self.PBUY)*100:
			self.runs[-1] += 1
			return Operation(Operation.BUY_OP, self.buy_amt)
		else:
			self.runs[-1] += 1
			return Operation(Operation.NONE_OP, 0)
			
