##used to store stat information for a particular buy sell pair

from db_manager import DBManager
import sqlite3


class StratStat:
	
	BUY_RATE = "buy_rate"
	SELL_RATE = "sell_rate"
	VOLUME = "volume"
	VOLATILITY = "volatility"
	
	def __init__(self, table_name, buy_rate, buy_candle_index):
		self.table_name = table_name
		self.buy_rate = buy_rate
		self.buy_candle_index = buy_candle_index
		self.sell_rate = 0
		self.volume = 0
		self.volatility = 0

	def update_values(self, sell_rate, volume, stddev):
		self.sell_rate = sell_rate
		self.volume = volume
		self.volatility = stddev

	def pprint(self):
		print("{:>20} Volume: {:>20} Volatility: {:>20}".format(self.sell_rate- self.buy_rate, self.volume, self.volatility))

	##inserts stratstat into db
	def save(self, to_commit = False):
		dbm = DBManager.get_instance()
		cursor = dbm.get_cursor()
		try:
			exec_string = "INSERT INTO {tn} ({nf_buy_rate}, {nf_sell_rate}, {nf_volume}, {nf_volatility}) VALUES\
					({v_buy_rate}, {v_sell_rate}, {v_volume}, '{v_volatility}')"\
				.format(tn = self.table_name, nf_buy_rate = StratStat.BUY_RATE, nf_sell_rate = StratStat.SELL_RATE, nf_volume = StratStat.VOLUME, nf_volatility = StratStat.VOLATILITY, v_buy_rate = self.buy_rate, v_sell_rate = self.sell_rate, v_volume = self.volume, v_volatility = self.volatility)
			cursor.execute(exec_string)
			
			##for speed purposes only commit when changing one at a time
			if to_commit:
				dbm.conn.commit()

		except sqlite3.IntegrityError:
			pass 
			##print('ERROR: Something went wrong inserting trade into {tn}'.format(tn = self.table_name))
		dbm.save_and_close()

