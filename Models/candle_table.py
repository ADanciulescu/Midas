## used to get info about candle table and create new candle tables

from db_manager import DBManager

class CandleTable:
	
	ID = "id"
	DATE = "date"
	HIGH = "high"
	LOW = "low"
	OPEN = "open"
	CLOSE = "close"
	MID = "mid"
	VOLUME = "volume"
	QUOTE_VOLUME = "quoteVolume"
	WEIGHTED_AVERAGE = "weightedAverage"

	def __init__(self, curr_ref, curr_target, start, end, period):
		self.curr_ref = curr_ref
		self.curr_target = curr_target
		self.start = start
		self.end = end
		self.period = period
		self.table_name = self.calc_table_name(curr_ref, curr_target, start, end, period)

	def save(self):
		self.create_candle_table()
	
	##calculate correctly formatted table_name from configuration
	@staticmethod
	def calc_table_name(curr_ref, curr_target, start, end, period):
		return "{cr}_{ct}_{s}_{e}_{p}".format(cr = curr_ref,ct = curr_target, s = start, e = end, p = period)


	
	##creates table for candle data
	##each row is a candle and holds data about the candle 
	##columns: id, date, high, low, open, close, volume, quoteVolume, weightedAverage
	def create_candle_table(self):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY {nn}, {nf_date} {ft_i} {nn}, {nf_high} {ft_r} {nn}, {nf_low} {ft_r} {nn}, {nf_open} {ft_r} {nn}, {nf_close} {ft_r} {nn}, {nf_mid} {ft_r} {nn}, {nf_volume} {ft_r} {nn}, {nf_qVol} {ft_r} {nn}, {nf_wAvg} {ft_r} {nn})'\
				.format(tn = self.table_name, nf_id = self.ID, nf_date = self.DATE, nf_high = self.HIGH, nf_low = self.LOW, nf_open = self.OPEN, nf_close = self.CLOSE, nf_mid = self.MID, nf_volume = self.VOLUME, nf_qVol = self.QUOTE_VOLUME, nf_wAvg = self.WEIGHTED_AVERAGE, ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, nn = DBManager.NOT_NULL)
		print exec_string
		cursor.execute(exec_string)
		db_manager.save_and_close()
	
	
	## drops the table by name
	@staticmethod	
	def drop_table(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		cursor.execute('DROP TABLE ' + table_name)
		db_manager.save_and_close()

	##returns true if table exists otherwise false
	@staticmethod	
	def exists_table(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}'".format(tn = table_name)
		cursor.execute(exec_string)
		if cursor.fetchone() is not None:
			return True
		else:
			return False
		db_manager.save_and_close()

	##returns currency name of the reference currency that the other is measured in terms of
	@staticmethod
	def get_ref_currency(table_name):
		info = table_name.split("_")
		return info[0]

	@staticmethod
	def get_target_currency(table_name):
		info = table_name.split("_")
		return info[1]
	
	@staticmethod
	def get_start_time(table_name):
		info = table_name.split("_")
		return info[2]
	
	@staticmethod
	def get_end_time(table_name):
		info = table_name.split("_")
		return info[3]
	
	@staticmethod
	def get_period(table_name):
		info = table_name.split("_")
		return info[4]
