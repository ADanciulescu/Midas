import json
import sqlite3
import threading

class DBManager:

	INSTANCES = []

	INTEGER = "INTEGER"
	REAL = "REAL"
	TEXT = "TEXT"
	NOT_NULL = "NOT NULL"
	
	def __init__(self, t_id):
		self.sqlfile = "./db/currencies.sqlite"
		self.conn = sqlite3.connect(self.sqlfile)
		self.thread_id = t_id
		self.lock = threading.Lock()

	@classmethod
	def get_instance(cls):
		cur_thread_id = threading.current_thread()
		ret = None
		for i in cls.INSTANCES:
			if i.thread_id == cur_thread_id:
				ret = i
		
		if ret is None:
			instance = cls(cur_thread_id)
			instance.open()
			DBManager.INSTANCES.append(instance)
			ret = instance

		if ret.lock.locked():
			ret.lock.release()
		ret.lock.acquire()
		return ret

	def open(self):
		self.conn = sqlite3.connect(self.sqlfile)

	def close(self):
		self.conn.close()

	##commit changes to db and close DBManager instance
	def save_and_close(self):
		self.conn.commit()
		self.lock.release()

	def get_cursor(self):
		return self.conn.cursor()

	## drops the table by name
	@staticmethod	
	def drop_table(table_name):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		cursor.execute('DROP TABLE ' + table_name)
		db_manager.save_and_close()
	
	## drops all tables that contain the given string
	@staticmethod	
	def drop_matching_tables(s):
		db_manager = DBManager.get_instance()

		##fetch all tables
		cursor = db_manager.get_cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		all_table_names = cursor.fetchall()

		for tn in all_table_names:
			if s in tn[0]:
				cursor.execute('DROP TABLE ' + tn[0])
		db_manager.save_and_close()

	##returns true if table exists otherwise false
	@staticmethod	
	def exists_table(table_name):
		db_manager = DBManager.get_instance()
		cursor = db_manager.get_cursor()
		exec_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}'".format(tn = table_name)
		cursor.execute(exec_string)
		if cursor.fetchone() is not None:
			return True
		else:
			return False
