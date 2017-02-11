##uses oscillators to tell when to buy or sell

from trade_simulator import TradeSimulator
from candle_table import CandleTable
from point_populator import PointPopulator
from operation import Operation

class OscilStrategy():

	NAME = "BOLLINGER"
	OSCIL_PERIOD = 40
	
	def __init__(self, table_name):
		self.candle_table_name = table_name
		self.candles = CandleTable.get_candle_array(table_name)
		self.amount = TradeSimulator.get_currency_amount(table_name)
		self.create_tables()

	def create_tables(self):
		pp = PointPopulator(self.candle_table_name)
		pp.setup()
		self.oscil_pts = pp.create_oscil(self.OSCIL_PERIOD)

	def decide(self, candle_num, bits):
		if candle_num <= self.OSCIL_PERIOD:
			return Operation(Operation.NONE_OP, 0)
		else:
			##if crossed 0 from below up, buy signal
			if self.oscil_pts[candle_num - self.OSCIL_PERIOD- 1].value < 0 and self.oscil_pts[candle_num - self.OSCIL_PERIOD].value > 0:
				return Operation(Operation.BUY_OP, self.amount)
			elif self.oscil_pts[candle_num - self.OSCIL_PERIOD- 1].value > 0 and self.oscil_pts[candle_num - self.OSCIL_PERIOD].value < 0:
				return Operation(Operation.SELL_OP, self.amount)
			else:
				return Operation(Operation.NONE_OP, 0)
				

		
	##simply returns name
	def get_name(self):
		return  self.NAME





