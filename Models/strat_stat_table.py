## a table containing strat stat 
## can be used to find patterns between profit and volatility/volume 
## columns: id, buy_rate, sell_rate, volume, volatility
from db_manager import DBManager
from strat_stat import StratStat
from candle_table import CandleTable

class StratStatTable:


	def __init__(self, table_name):
		self.table_name = table_name
	
	
	##creates stratstat table in db
	def save(self):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_buy_rate} {ft_r} {nn}, {nf_sell_rate} {ft_r} {nn}, {nf_volume} {ft_r} {nn}, {nf_volatility} {ft_r} {nn})'\
				.format(tn = self.table_name, nf_buy_rate = StratStat.BUY_RATE, nf_sell_rate = StratStat.SELL_RATE, nf_volume = StratStat.VOLUME, nf_volatility = StratStat.VOLATILITY, ft_r = DBManager.REAL, nn = DBManager.NOT_NULL)
		cursor.execute(exec_string)
		dbm.save_and_close()
	
	
	##returns name for trade table
	@staticmethod
	def calc_name(candle_table_name, strategy_name):
		return "STRATSTAT_"+ strategy_name + "_" + CandleTable.get_target_currency(candle_table_name) + "_" + CandleTable.get_period(candle_table_name)

