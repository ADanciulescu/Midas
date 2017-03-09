## puts trades in a table so that they can be tracked

from candle_table import CandleTable
from db_manager import DBManager
from trade_table import TradeTable
from trade import Trade

class TradeLogger:

	##creates full table of empty trades to be updated later by calling log_trade
	def __init__(self, table_name, candle_table_name):
		self.table_name = table_name
		self.candle_table_name = candle_table_name

		if dbm.exists_table(table_name):
			DBManager.drop_table(table_name)
		self.table = TradeTable(table_name)
		self.table.save()

		candles = CandleTable.get_candle_array(candle_table_name)
		for c in candles:
			p = Trade(dbm, table_name, c.date, 0, 0, Trade.NONE_TYPE)
			p.save()
		dbm = DBManager.get_instance()
		dbm.save_and_close()
		
	def log_trade(self, date, amount, price, type):
		trade = TradeTable.get_trade(self.table_name, date)
		trade.amount = amount
		trade.price = price
		trade.type = type
		trade.update()



