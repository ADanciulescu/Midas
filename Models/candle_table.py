## used to get info about candle table and create new candle tables
	##each row is a candle and holds data about the candle 
	##columns: id, date, high, low, open, close, volume, quoteVolume, weightedAverage

from db_manager import DBManager
from point_table import PointTable
from point import Point
from candle import Candle

class CandleTable:
	
	CANDLE = "CANDLE"
	TEMP = "TEMP"

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
		return "{c}_{cr}_{ct}_{s}_{e}_{p}".format(c = CandleTable.CANDLE, cr = curr_ref,ct = curr_target, s = start, e = end, p = period)


	##creates candle table in db
	def create_candle_table(self):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		exec_string = 'CREATE TABLE {tn} ({nf_id} {ft_i} PRIMARY KEY {nn}, {nf_date} {ft_i} {nn}, {nf_high} {ft_r} {nn}, {nf_low} {ft_r} {nn}, {nf_open} {ft_r} {nn}, {nf_close} {ft_r} {nn}, {nf_mid} {ft_r} {nn}, {nf_volume} {ft_r} {nn}, {nf_qVol} {ft_r} {nn}, {nf_wAvg} {ft_r} {nn})'\
				.format(tn = self.table_name, nf_id = self.ID, nf_date = self.DATE, nf_high = self.HIGH, nf_low = self.LOW, nf_open = self.OPEN, nf_close = self.CLOSE, nf_mid = self.MID, nf_volume = self.VOLUME, nf_qVol = self.QUOTE_VOLUME, nf_wAvg = self.WEIGHTED_AVERAGE, ft_i = DBManager.INTEGER, ft_r = DBManager.REAL, nn = DBManager.NOT_NULL)
		print exec_string
		cursor.execute(exec_string)
		db_manager.save_and_close()
	
	
	##returns cursor to all candles in table_name)
	@staticmethod
	def get_candle_cursor(table_name):
		db_manager = DBManager()
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT * FROM '{tn}'".format(tn = table_name))
		return cursor


	## return last date
	@staticmethod
	def get_first_date(table_name):
		dbm = DBManager()
		cursor = dbm.get_cursor()
		cursor.execute(" SELECT date FROM '{tn}' WHERE date = ( SELECT MIN(date) FROM '{tn}' )".format(tn = table_name))
		return cursor.fetchone()

	## return first date
	@staticmethod
	def get_last_date(table_name):
		dbm = DBManager()
		cursor = dbm.get_cursor()
		cursor.execute(" SELECT date FROM '{tn}' WHERE date = ( SELECT MAX(date) FROM '{tn}' )".format(tn = table_name))
		return cursor.fetchone()

	##returns currency name of the reference currency that the other is measured in terms of
	@staticmethod
	def get_ref_currency(table_name):
		info = table_name.split("_")
		return info[0]

	@staticmethod
	def get_target_currency(table_name):
		info = table_name.split("_")
		return info[2]
	
	@staticmethod
	def get_start_time(table_name):
		info = table_name.split("_")
		return info[1]
	
	@staticmethod
	def get_end_time(table_name):
		info = table_name.split("_")
		return info[3]
	
	@staticmethod
	def get_period(table_name):
		info = table_name.split("_")
		return info[4]


	##create point table using date and mid from candle_table_name, return its name
	@staticmethod
	def to_point_table(candle_table_name):
		pt_name = CandleTable.TEMP + "_" + candle_table_name
		
		##if already exists, drop it first and then recreate
		if DBManager.exists_table(pt_name):
			DBManager.drop_table(pt_name)
		
		pt = PointTable(pt_name)
		pt.save()
		candles = CandleTable.get_candle_array(candle_table_name)
		dbm = DBManager()
		for c in candles:
			p = Point(dbm, pt_name, c.date, c.mid)
			p.save()
		dbm.save_and_close()
		return pt_name
	
	##returns candle objects for the given table_name
	@staticmethod
	def get_candle_array(table_name):

		##returns a cursor pointing to all candles linked to the table_name
		cursor = CandleTable.get_candle_cursor(table_name)
	
		candles = []

		##loop through cursor and add all candles to array
		row = cursor.fetchone()
		while row is not None:
			t = Candle.from_tuple(table_name, row) 
			candles.append(t)
			row = cursor.fetchone()
		return candles
